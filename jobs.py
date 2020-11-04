from datetime import datetime
from db import (db, get_financial_currency, get_financial_stocks, get_notificated_user, find_currency_value,
                stop_notifications)
from settings import CURRENCY_LIST, STOCKS_LIST

import yfinance as yf


def get_financial_assets(context):
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    financial_assets = {'currency': CURRENCY_LIST, 'stocks': STOCKS_LIST}
    for assets in financial_assets:
        if assets == 'currency':
            for asset in financial_assets['currency']:
                get_financial_currency(db, date_str, get_yahoo_finance_currency(asset), asset)
        elif assets == 'stocks':
            for asset in financial_assets['stocks']:
                get_financial_stocks(db, date_str, get_yahoo_finance_stocks(asset), asset)


def get_yahoo_finance_currency(asset):
    price = yf.download(f'{asset}RUB=X', datetime.now())['Close'][-1]
    return price


def get_yahoo_finance_stocks(asset):
    price = yf.download(asset, datetime.now())['Close'][-1]
    return price

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
            time.sleep(60)
            continue
        text = f'{currency} стал меньше {user_currency_value} руб.'
        stop_notifications(db, user['chat_id'])
        return context.bot.send_message(chat_id=user['chat_id'], text=text)
    if currency_db['value'] < user_currency_value:
        while currency_db['value'] < user_currency_value:
            currency_db = find_currency_value(db, currency)
            time.sleep(5)
            continue
        text = f'{currency} стал больше {user_currency_value} руб.'
        stop_notifications(db, user['chat_id'])
        return context.bot.send_message(chat_id=user['chat_id'], text=text)