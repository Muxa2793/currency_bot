from datetime import datetime
from db import db, get_financial_currency, get_financial_stocks

import yfinance as yf


def get_financial_assets(context):
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")   
    financial_assets = {'currency': ['USDRUB=X', 'EURRUB=X'], 'stock': ['YNDX']}
    for assets in financial_assets:
        if assets == 'currency':
            for asset in financial_assets['currency']:
                get_financial_currency(db, date_str, get_yahoo_finance(asset), asset)
        elif assets == 'stock':
            for asset in financial_assets['stock']:
                get_financial_stocks(db, date_str, get_yahoo_finance(asset), asset)


def get_yahoo_finance(asset):
    date = datetime.now()
    price = yf.download(asset, date)['Close'][-1]
    return price
