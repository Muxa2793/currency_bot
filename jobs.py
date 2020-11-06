from datetime import datetime
from db import (db, get_financial_currency, get_financial_stocks, get_notificated_user, find_currency_value,
                stop_notifications)
from settings import CURRENCY_LIST, STOCKS_LIST
from telegram.error import BadRequest

import time
import yfinance as yf


def get_financial_assets(context):
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    financial_assets = {'currency': CURRENCY_LIST, 'stock': STOCKS_LIST}
    for asset in financial_assets.get('currency', []):
        get_financial_currency(db, date_str, get_yahoo_finance_currency(asset), asset)
    for asset in financial_assets.get('stock', []):
        get_financial_stocks(db, date_str, get_yahoo_finance_stock(asset), asset)


def get_yahoo_finance_currency(asset):
    return yf.download(f'{asset}RUB=X', datetime.now())['Close'][-1]


def get_yahoo_finance_stock(asset):
    return yf.download(asset, datetime.now())['Close'][-1]


def send_notifications(context):
    for user in get_notificated_user(db):
        try:
            check_value(context, user)
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден")


def check_value(context, user):
    currency = user['notification_settings']['asset']
    currency_db = find_currency_value(db, currency)
    user_currency_value = user['notification_settings']['notification_value']
    if currency_db['value'] > user_currency_value:
        while currency_db['value'] > user_currency_value:
            currency_db = find_currency_value(db, currency)
            time.sleep(20)
        text = f'{currency} стал меньше {user_currency_value} руб.'
        stop_notifications(db, user['chat_id'])
        return context.bot.send_message(chat_id=user['chat_id'], text=text)
    elif currency_db['value'] < user_currency_value:
        while currency_db['value'] < user_currency_value:
            currency_db = find_currency_value(db, currency)
            time.sleep(20)
        text = f'{currency} стал больше {user_currency_value} руб.'
        stop_notifications(db, user['chat_id'])
        return context.bot.send_message(chat_id=user['chat_id'], text=text)
