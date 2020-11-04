import logging
from db import db, get_or_create_user, find_currency_value, find_stocks_value, create_notifications_settings
from utils import main_keyboard, user_currency_keyboard, user_stocks_keyboard
from settings import CURRENCY_LIST, STOCKS_LIST
from telegram.ext import ConversationHandler


def greet_user(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    logging.info('Вызван /start')
    currency_list = ', '.join(CURRENCY_LIST)
    stocks_list = ', '.join(STOCKS_LIST)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют, '
      'акций и криптовалют.\n\n'
      '/settings - для настройки бота\n\n'
      '/notifications <валюта> <значение> - для настройки выдачи уведомлений.'
      'Например: комманда </notifications USD 75.4> '
      'выдаст вам уведомление если курс валюты станет больше или меньше 75.4 рублей\n\n'
      f'Список доступных валют: {currency_list}\n' 
      f'Список доступных акций: {stocks_list}',
      reply_markup=main_keyboard()
    )


def choose_currency(update, context):
    update.message.reply_text('Выберите валюту',
                              reply_markup=user_currency_keyboard(update))
    return 'currency_price'

def choose_stocks(update, context):
    update.message.reply_text('Выберите акцию',
                              reply_markup=user_stocks_keyboard(update))
    return 'stocks_price'


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

def get_stocks_price(update, context): ###
    if update.message.text in STOCKS_LIST:
        user_currency = update.message.text
        stocks_db = find_stocks_value(db, update.message.text)
        value = stocks_db['value']
        value = round(value, 3)
        date = stocks_db['date']
        update.message.reply_text(f'{user_currency}: {value} на {date}')
    elif update.message.text == 'Вернуться':
        update.message.reply_text('Выберете актив',
                                  reply_markup=main_keyboard())
        return ConversationHandler.END

def currency_db_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')


def add_notifications_settings(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_text = context.args
    currency_list = ', '.join(CURRENCY_LIST)
    asset = user_text[0].upper()
    value = user_text[1]
    if asset not in CURRENCY_LIST:
        update.message.reply_text(f'Такой валюты нет. Пожалуйста введите валюту из списка: {currency_list}')
    elif value:
        try:
            value = float(value.replace(',', '.'))
            create_notifications_settings(db, update.effective_user, asset, value)
            update.message.reply_text(f'Если {asset} станет больше или меньше {value} руб., вам придёт уведомление.')
        except ValueError:
            update.message.reply_text('Укажите значение валюты как число, например 75.6')

def add_notifications_settings_stoks(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_text = context.args
    stocks_list = ', '.join(STOCKS_LIST)
    asset = user_text[0].upper()
    value = user_text[1]
    if asset not in STOCKS_LIST:
        update.message.reply_text(f'Такой акции нет. Пожалуйста введите акцию из списка: {stocks_list}')
    elif value:
        try:
            value = float(value.replace(',', '.'))
            create_notifications_settings(db, update.effective_user, asset, value)
            update.message.reply_text(f'Если {asset} станет больше или меньше {value}, вам придёт уведомление.')
        except ValueError:
            update.message.reply_text('Укажите значение стоимости например 75.6')