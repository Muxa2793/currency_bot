from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]


def get_financial_asset(db, date, price, financial_asset):
    currency_db = db.currency.find_one({"currency": financial_asset})
    stocks_db = db.stocks.find_one({"stocks": financial_asset})
    if currency_db:
        if not currency_db:
            currency_db = {
                "currency": financial_asset,
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
    elif stocks_db:  # проверка базы акций
        pass
