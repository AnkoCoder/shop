from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
updater = Updater(token='1115972626:AAH2Tnx3N3NRa0knkZJDedOS1Ny21RsbTxA', use_context=True)
dispatcher = updater.dispatcher


GENDER, AGE, AGAIN = range(3)


def start(update, context):
    keyboard = [
        [InlineKeyboardButton('Man', callback_data='man'),
         InlineKeyboardButton('Woman', callback_data='woman')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! Please, choose your gender",
        reply_markup=reply_markup
    )
    return GENDER

def gender(update, context):
    context.user_data['gender'] = update.callback_query.data
    keyboard = [
        [InlineKeyboardButton('10-20', callback_data='10-20'),
        InlineKeyboardButton('20-32', callback_data='20-32'),
        InlineKeyboardButton('32-45', callback_data='32-45')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose your age",
        reply_markup=reply_markup
    )
    return AGE

def age(update, context):
    context.user_data['age'] = update.callback_query.data
    age = context.user_data['age']
    gender = context.user_data['gender']
    message = 'Your gender is {} and age is in the range of {}. Do you want to talk again?'.format(gender, age)
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=message
    )
    return AGAIN

def again(update, context):
    if update.message.text.lower() == 'yes':
        return start(update, context)
    else: 
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='Ok! Maybe next time!'
        )
        return ConversationHandler.END # позволяет закончить разговор и не застрять в последней функции
        # тогда пользователь после завершения разговора может заново его начать и на надо для этого 
        # перезагружать бот

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GENDER: [CallbackQueryHandler(gender)],
        AGE: [CallbackQueryHandler(age)],
        AGAIN: [MessageHandler(Filters.text, again)]
    },
    fallbacks=[]
)


dispatcher.add_handler(conv_handler)


updater.start_polling()