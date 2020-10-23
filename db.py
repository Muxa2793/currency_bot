from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def get_financial_currency(db, date, price, asset):
    currency_db = db.currency.find_one({"currency": asset})
    if currency_db is None:
        currency_db = {
            "currency": asset,
            "value": price,
            "date": date,
        }
        db.currency.insert_one(currency_db)
    else:
        db.currency.update_one(
            {'_id': currency_db['_id']},
            {'$set': {'value': price, 'date': date}})
    return currency_db


def get_financial_stocks(db, date, price, asset):
    stocks_db = db.stocks.find_one({"stock": asset})
    if stocks_db is None:
        stocks_db = {
            "stock": asset,
            "value": price,
            "date": date,
        }
        db.stocks.insert_one(stocks_db)
    else:
        db.stocks.update_one(
            {'_id': stocks_db['_id']},
            {'$set': {'value': price, 'date': date}})
    return stocks_db
