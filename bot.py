import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app import db, Product, Order, OrderItem

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I am a shop bot. What would you like to buy?')

def products(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Check products on our website '  + 'http://127.0.0.1:5000/')

def add_to_cart(update, context):
    logging.info(update.message.from_user.id)
    order = Order(telegram_id=update.message.from_user.id) #записываю в таблицу Order
    db.session.add(order)
    product_name = context.args[0]
    quantity = context.args[1]
    logging.info(product_name)
    product = Product.query.filter(Product.name==product_name).first()
    item = OrderItem(product_id=product.id, quantity=int(quantity)) 
    db.session.add(item)
    db.session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id, text='The product is added to your cart. Do you want anything else?')
    #как указывать количество товара которое хочу купить сразу вместе с наименованием товара? 
    #как зациклить добавление товаров в карт по ответу да/нет. Если да, то функция повторяется, если нет, то выходит сообщение
    #с итоговой стоимостью всего что есть в карт

start_handler = CommandHandler('start', start)
products_handler = CommandHandler('products', products)
add_to_cart_handler = CommandHandler('add', add_to_cart)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(products_handler)
dispatcher.add_handler(add_to_cart_handler)

updater.start_polling()