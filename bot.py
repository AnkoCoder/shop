import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from app import db, Product, Order, OrderItem

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I am a shop bot. What would you like to buy?')

def add_to_cart(update, context):
    products = [product.name for product in Product.query.all()]
    products = '\n'.join(products)
    context.bot.send_message(chat_id=update.effective_chat.id, text=products)


start_handler = CommandHandler('start', start)
add_to_cart_handler = CommandHandler('products', add_to_cart)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_to_cart_handler)

updater.start_polling()