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


def create_stocks_list(db, effective_user, stocks_list):
    user = db.users.find_one({'user_id': effective_user.id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'stocks_list': stocks_list}})


def create_crypto_list(db, effective_user, crypto_list):
    user = db.users.find_one({'user_id': effective_user.id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'crypto_list': crypto_list}})


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
    stocks_db = db.stocks.find_one({"stocks": asset})
    if not stocks_db:
        stocks_db = {
            "stocks": asset,
            "value": price,
            "date": date,
        }
        db.stocks.insert_one(stocks_db)
    else:
        db.stocks.update_one(
            {'_id': stocks_db['_id']},
            {'$set': {'value': price, 'date': date}})
    return stocks_db


def get_financial_crypto(db, date, price, asset):
    crypto_db = db.crypto.find_one({"crypto": asset})
    if not crypto_db:
        crypto_db = {
            "crypto": asset,
            "value": price,
            "date": date,
        }
        db.crypto.insert_one(crypto_db)
    else:
        db.crypto.update_one(
            {'_id': crypto_db['_id']},
            {'$set': {'value': price, 'date': date}})
    return crypto_db


def get_user_currency_keyboard(db, effective_user):
    user = db.users.find_one({'user_id': effective_user.id})
    try:
        return user['currency_list']
    except KeyError:
        default_keyboard = ['USD', 'EUR']
        return default_keyboard


def get_user_stocks_keyboard(db, effective_user):
    user = db.users.find_one({'user_id': effective_user.id})
    try:
        return user['stocks_list']
    except KeyError:
        default_keyboard = ['YNDX', 'MSFT']
        return default_keyboard


def get_user_crypto_keyboard(db, effective_user):
    user = db.users.find_one({'user_id': effective_user.id})
    try:
        return user['crypto_list']
    except KeyError:
        default_keyboard = ['BTC', 'ETH']
        return default_keyboard


def find_currency_value(db, asset):
    return db.currency.find_one({"currency": asset})


def find_stocks_value(db, asset):
    return db.stocks.find_one({"stocks": asset})


def find_crypto_value(db, asset):
    return db.crypto.find_one({"crypto": asset})


def create_notifications_settings(db, effective_user, asset, value):
    user = db.users.find_one({'user_id': effective_user.id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'notificate': True,
                      'notification_settings': {'asset': asset, 'notification_value': value}}})


def get_notificated_user(db):
    return db.users.find({"notificate": True})


def stop_notifications(db, chat_id):
    user = db.users.find_one({'user_id': chat_id})
    if user:
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'notificate': False}})
