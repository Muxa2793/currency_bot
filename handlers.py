import logging
from db import db, get_or_create_user, find_currency_value, create_notifications_settings
from utils import main_keyboard, user_currency_keyboard
from settings import CURRENCY_LIST
from telegram.ext import ConversationHandler


def greet_user(update, context):
    logging.info('Вызван /start')

    get_or_create_user(db, update.effective_user, update.message.chat.id)
    currency_list = ', '.join(CURRENCY_LIST)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют, '
      'акций и криптовалют.\n\n'
      '/settings - для настройки бота\n\n'
      '/notice <валюта> <значение> - для настройки выдачи уведомлений.'
      'Например: комманда </notifications USD 75.4> '
      'выдаст вам уведомление если курс валюты станет больше или меньше 75.4 рублей\n\n'
      f'Список доступных валют: {currency_list}',
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


def add_notifications_settings(update, context):
    logging.info('Вызван /notice')

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
