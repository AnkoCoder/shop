import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func
from app import db, Product, Order, OrderItem


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    button_list = [
        [
            InlineKeyboardButton("Visit shop", url='http://127.0.0.1:5000/'),
            InlineKeyboardButton("Add to cart", callback_data='add'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Dear customer! Welcome to our online shop. You can check our products on the website ' +
        ' If you want to add a product to your cart use /add command', 
        reply_markup=reply_markup
    )

# Проверяет есть ли такой номер заказа в таблице. 
# Если есть, то все заказы до момента завершения общения с ботом будут записаны под этим номером 
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
        text='Type in the name or ID of the product you want to add to your cart.'
    )
    return ADD_TO_CART

def add_to_cart(update, context):
    try:
        product_id = int(update.message.text)
        product = Product.query.filter(Product.id==product_id).first()
    except ValueError:
        product_name = update.message.text
        products = list(Product.query.filter(func.lower(Product.name).contains(product_name)))
        if len(products) > 1:
            message = 'Found following products:\n'
            for product in products:
                message += '\n{} with ID = {}'.format(product.name, product.id)
            message += '\n\nType in the name or ID of the product you want to add to your cart.'
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=message
            )
            return ADD_TO_CART
        else:
            product = products[0]
    context.user_data['product_id'] = product.id
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='How many {} do you want?'.format(product.name)
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
    keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes'),
        InlineKeyboardButton('No', callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text= '{} in quantity of {} added to your cart! Do you want to add anything else?'.format(product.name, quantity),
        reply_markup=reply_markup
    )
    return AGAIN


def again(update, context):
    if update.callback_query.data == 'yes':
        return choose_product(update, context)
    else:
        return end(update, context)


def end(update, context):
    order_id = context.user_data['order_id']    
    message = 'Your order id is ' + str(order_id) + '. Your cart: \n\n'
    items = OrderItem.query.filter(OrderItem.order_id==order_id).all()
    message += '\n'.join(
        'Product: {}, quantity: {}, price in USD: {}'.format(item.product.name, item.quantity, item.product.cost) for item in items
    )
    message += '\n\nTotal cost: {} USD'.format(str(sum(item.quantity * item.product.cost for item in items)))
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=message
    )
    del context.user_data['order_id']
    return ConversationHandler.END


start_handler = CommandHandler('start', start)
conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(choose_product, pattern='add'), 
        CommandHandler('add', choose_product)
    ],

    states={
        ADD_TO_CART: [MessageHandler(Filters.text, add_to_cart)],
        QUANTITY: [MessageHandler(Filters.text, quantity)],
        AGAIN: [CallbackQueryHandler(again)],
        END: [MessageHandler(Filters.text, end)]
    }, 

    fallbacks=[]
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)


updater.start_polling()



