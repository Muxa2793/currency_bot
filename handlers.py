import logging
from db import db, get_or_create_user, find_currency_value
from utils import main_keyboard, user_currency_keyboard
from settings import CURRENCY_LIST
from telegram.ext import ConversationHandler


def greet_user(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    logging.info('Вызван /start')
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют,'
      'акций и криптовалют.\n'
      '/settings - для настройки бота\n'
      'Также в нём скоро появятся другие крутые фишки.',
      reply_markup=main_keyboard()
    )


def choose_currency(update, context):
    update.message.reply_text('Выберите валюту',
                              reply_markup=user_currency_keyboard(update))
    return 'currency_price'


def get_currency_price(update, context):
    if update.message.text in CURRENCY_LIST:
        user_currency = update.message.text
        currency_db = find_currency_value(db, update.message.text)
        value = currency_db['value']
        value = round(value, 3)
        date = currency_db['date']
        update.message.reply_text(f'{user_currency}: {value} руб. на {date}')
    elif update.message.text == 'Вернуться':
        update.message.reply_text('Выберете актив',
                                  reply_markup=main_keyboard())
        return ConversationHandler.END


def currency_db_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')


'''
def currency_transfer(user_currency):
    if user_currency == 'USD':
        currency_transfer = 'USDRUB=X'
    elif user_currency == 'EUR':
        currency_transfer = 'EURRUB=X'
    return currency_transfer
'''
