from datetime import datetime
from db import db, get_financial_currency, get_financial_stocks
from settings import CURRENCY_LIST

import yfinance as yf


def get_financial_assets(context):
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    financial_assets = {'currency': CURRENCY_LIST, 'stock': ['YNDX']}
    for assets in financial_assets:
        if assets == 'currency':
            for asset in financial_assets['currency']:
                get_financial_currency(db, date_str, get_yahoo_finance_currency(asset), asset)
        elif assets == 'stock':
            for asset in financial_assets['stock']:
                get_financial_stocks(db, date_str, get_yahoo_finance_stock(asset), asset)


def get_yahoo_finance_currency(asset):
    price = yf.download(f'{asset}RUB=X', datetime.now())['Close'][-1]
    return price


def get_yahoo_finance_stock(asset):
    price = yf.download(asset, datetime.now())['Close'][-1]
    return price
