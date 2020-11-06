import logging
from db import (db, get_or_create_user, find_currency_value, find_stocks_value, find_crypto_value,
                create_notifications_settings)
from utils import (main_keyboard, user_currency_keyboard, user_stocks_keyboard,
                    user_crypto_keyboard)
from settings import CURRENCY_LIST, STOCKS_LIST, CRYPTO_LIST
from telegram.ext import ConversationHandler


def greet_user(update, context):
    logging.info('Вызван /start')

    get_or_create_user(db, update.effective_user, update.message.chat.id)
    currency_list = ', '.join(CURRENCY_LIST)
    stocks_list = ', '.join(STOCKS_LIST)
    crypto_list = ', '.join(CRYPTO_LIST)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют, '
      'акций и криптовалют.\n\n'
      '/settings - для настройки бота\n\n'
      '/notice <актив> <значение> - для настройки выдачи уведомлений.'
      'Например: комманда </notifications USD 75.4> '
      'выдаст вам уведомление если курс валюты станет больше или меньше 75.4 рублей\n\n'
      f'Список доступных валют: {currency_list}\n'
      f'Список доступных акций: {stocks_list}\n'
      f'Список доступных криптовалют: {crypto_list}',      
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


def choose_crypto(update, context):
    update.message.reply_text('Выберите криптовалюту',
                              reply_markup=user_crypto_keyboard(update))
    return 'crypto_price'


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


def get_stocks_price(update, context):
    if update.message.text in STOCKS_LIST:
        user_stocks = update.message.text
        stocks_db = find_stocks_value(db, update.message.text)
        value = stocks_db['value']
        value = round(value, 3)
        date = stocks_db['date']
        update.message.reply_text(f'{user_stocks}: {value} $ на {date}')
    elif update.message.text == 'Вернуться':
        update.message.reply_text('Выберете актив',
                                  reply_markup=main_keyboard())
        return ConversationHandler.END


def get_crypto_price(update, context):
    if update.message.text in CRYPTO_LIST:
        user_crypto = update.message.text
        crypto_db = find_crypto_value(db, update.message.text)
        value = crypto_db['value']
        value = round(value, 3)
        date = crypto_db['date']
        update.message.reply_text(f'{user_crypto}: {value} $ на {date}')
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
    stocks_list = ', '.join(STOCKS_LIST)
    crypto_list = ', '.join(CRYPTO_LIST)
    asset = user_text[0].upper()
    value = user_text[1]
    if asset not in CURRENCY_LIST and asset not in STOCKS_LIST and asset not in CRYPTO_LIST:
        update.message.reply_text('Такого актива нет. Пожалуйста выберите актив из списка:\n'
                                  f'Валюта: {currency_list}\n'
                                  f'Акции: {stocks_list}\n'
                                  f'Криптовалюта: {crypto_list}')
    elif asset in CURRENCY_LIST:
        sign = 'руб.'
        set_notice(asset, value, update, sign)
    elif asset in STOCKS_LIST or asset in CRYPTO_LIST :
        sign = '$'
        set_notice(asset, value, update, sign)


def set_notice(asset, value, update, sign):
    try:
        value = float(value.replace(',', '.'))
        create_notifications_settings(db, update.effective_user, asset, value)
        update.message.reply_text(f'Если {asset} станет больше или меньше {value} {sign}, вам придёт уведомление.')
    except ValueError:
        update.message.reply_text('Укажите стоимость актива как число, например 80.6')
