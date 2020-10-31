from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({'user_id': effective_user.id})
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'username': effective_user.username,
            'chat_id': chat_id
        }
        db.users.insert_one(user)
    return user


def create_currency_list(db, effective_user, currency_list):
    user = db.users.find_one({'user_id': effective_user.id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'currency_list': currency_list}})


def get_financial_currency(db, date, price, asset):
    currency_db = db.currency.find_one({"currency": asset})
    if not currency_db:
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
    if not stocks_db:
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


def get_user_currency_keyboard(db, effective_user):
    user = db.users.find_one({'user_id': effective_user.id})
    return user['currency_list']


def find_currency_value(db, asset):
    currency_db = db.currency.find_one({"currency": asset})
    return currency_db


def create_notifications_settings(db, effective_user, asset, value):
    user = db.users.find_one({'user_id': effective_user.id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'notification_settings': {'asset': f'{asset}RUB=X', 'notification_value': value}}})
