from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def get_currency(db, date, price, current_currency):
    currency_db = db.currency.find_one({"currency": current_currency})
    if not currency_db:
        currency_db = {
            "currency": current_currency,
            "value": price,
            "date": date,
        }
        db.currency.insert_one(currency_db)
    elif currency_db:
        db.currency.update_one(
            {'_id': currency_db['_id']},
            {'$set': {'value': price, 'date': date}},
        )
    return currency_db
