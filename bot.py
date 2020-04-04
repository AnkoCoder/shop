import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app import db, Product, Order, OrderItem

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    button = InlineKeyboardButton("Visit shop", url='http://127.0.0.1:5000/')
    reply_markup = InlineKeyboardMarkup([[ button ]])
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Dear customer! Welcome to our online shop. You can check our products on the website ' +
        ' If you want to add a product to your cart use /add command', 
        reply_markup=reply_markup
    )


def get_or_create_order(update, context):
    user_data = context.user_data
    if 'order_id' in user_data:
        order_id = user_data['order_id']
        order = Order.query.filter(Order.id==order_id).first()
    else:
        order = Order(telegram_id=update.message.from_user.id) 
        db.session.add(order)
        db.session.commit()
        user_data['order_id'] = order.id
    return order

ADD_TO_CART  = 0
QUANTITY = 1
AGAIN = 2
END = 3

def choose_product(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Type in the name of the product you want to add to your cart.'
    )
    return ADD_TO_CART

def add_to_cart(update, context):
    product_name = update.message.text
    product = Product.query.filter(Product.name==product_name).first()
    context.user_data['product_id'] = product.id
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='How many ' + product_name + ' do you want?'
    )
    return QUANTITY


def quantity(update, context):
    order = get_or_create_order(update, context)
    quantity = int(update.message.text)
    product_id = context.user_data['product_id']
    product = Product.query.filter(Product.id==product_id).first()
    item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text= product.name + 
        ' in quantity of ' + 
        str(quantity) + 
        ' added to your cart! If you want to add anything else type "yes", othewise type "no"?'
    )
    return AGAIN


def again(update, context):
    if update.message.text == 'yes':
        return choose_product(update, context)
    elif update.message.text == 'no':
        return end(update, context)


def end(update, context):
    order_id = context.user_data['order_id']    
    message = 'Your order id is ' + str(order_id) + '. Your cart: \n\n'
    items = OrderItem.query.filter(OrderItem.order_id==order_id).all()
    message += '\n'.join(
        '{} {} {}'.format(item.product.name, item.quantity, item.product.cost) for item in items
    )
    message += '\n\nTotal: ' + str(sum(item.quantity * item.product.cost for item in items))
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=message
    )
    del context.user_data['order_id']
    return start(update, context)


start_handler = CommandHandler('start', start)
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', choose_product)],

    states={
        ADD_TO_CART: [MessageHandler(Filters.text, add_to_cart)],
        QUANTITY: [MessageHandler(Filters.text, quantity)],
        AGAIN: [MessageHandler(Filters.text, again)],
        END: [MessageHandler(Filters.text, end)]
    }, 

    fallbacks=[]
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)


updater.start_polling()



