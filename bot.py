import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from app import db, Product, Order, OrderItem

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Dear customer! Welcome to our online shop. You can check our products on the website ' + 'http://127.0.0.1:5000/' + ' If you want to add a product to your cart use /add command')

ADD_TO_CART  = 0
AGAIN = 1
END = 2

def choose_product(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='If you want to add something to your cart you need to type the name of the product and the quantity you want to buy (Example: Pants, 1). Otherwise type "no".')
    return ADD_TO_CART

def add_to_cart(update, context):
    if update.message.text == 'no':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Maybe next time you will be in mood for shopping :-)')
        return end(update, context)
    else:
        logging.info(update.message.text)
        order = Order(telegram_id=update.message.from_user.id) 
        db.session.add(order)
        product_name = update.message.text.split(',')
        logging.info(product_name)
        product = Product.query.filter(Product.name==product_name[0]).first()
        item = OrderItem(product_id=product.id, quantity=int(product_name[1])) 
        db.session.add(item)
        db.session.commit()
        context.bot.send_message(chat_id=update.effective_chat.id, text='The product is added to your cart. If you want to ass anything else to your cart type "yes"?')
    return AGAIN


def again(update, context):
    if update.message.text == 'yes':
        return choose_product(update, context)
    elif update.message.text == 'no':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Maybe next time you will be in mood for shopping :-)')
        return end(update, context)

def end(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='It was nice talking to you! See you soon!')
    return END

start_handler = CommandHandler('start', start)
#add_to_cart_handler = CommandHandler('add', add_to_cart)
choose_product_handler = CommandHandler('how', choose_product)

dispatcher.add_handler(start_handler)
#dispatcher.add_handler(add_to_cart_handler)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', choose_product)],

    states={
        ADD_TO_CART: [MessageHandler(Filters.text, add_to_cart)],
        AGAIN: [MessageHandler(Filters.text, again)],
        END: [MessageHandler(Filters.text, end)]
    }, 

    fallbacks=[]
)

dispatcher.add_handler(conv_handler)

updater.start_polling()



# def add_to_cart(update, context):
#     order = Order(telegram_id=update.message.from_user.id) 
#     db.session.add(order)
#     product_name = context.args[0]
#     quantity = context.args[1]
#     product = Product.query.filter(Product.name==product_name).first()
#     item = OrderItem(product_id=product.id, quantity=int(quantity)) 
#     db.session.add(item)
#     db.session.commit()
#     context.bot.send_message(chat_id=update.effective_chat.id, text='The product is added to your cart. Do you want anything else?')
