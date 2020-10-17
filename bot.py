import logging
import settings
import yfinance as yf
from datetime import datetime
from db import db, get_financial_asset_db
from tasks import run_scheduler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    logging.info('Вызван /start')
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют,'
      'акций и криптовалют.\n'
      'Также в нём скоро появятся другие крутые фишки.',
      reply_markup=main_keyboard()
    )


def currency_price(update, context):
    currency_list = ['USD', 'EUR']
    if update.message.text == 'Валюта':
        update.message.reply_text('Выберите валюту',
                                  reply_markup=currency_keyboard())
    if update.message.text == 'Вернуться':
        update.message.reply_text('Что вы хотите узнать?',
                                  reply_markup=main_keyboard())
    if update.message.text in currency_list:
        user_currency = update.message.text
        currency = currency_transfer(update.message.text)
        financial_asset_db = get_financial_assets(currency)
        value = financial_asset_db['value']
        # value = round(value, 3)
        date = financial_asset_db['date']
        update.message.reply_text(f'{user_currency}: {value} руб. на {date}')


def currency_transfer(user_currency):
    if user_currency == 'USD':
        currency_transfer = 'USDRUB=X'
    elif user_currency == 'EUR':
        currency_transfer = 'EURRUB=X'
    return currency_transfer


def get_financial_assets(financial_asset):
    date = datetime.now()
    price = yf.download(financial_asset, date)['Close'][-1]
    date = date.strftime("%d.%m.%Y %H:%M")
    financial_asset_db = get_financial_asset_db(db, date, price,
                                                financial_asset)
    return financial_asset_db


def currency_keyboard():
    return ReplyKeyboardMarkup([
                                ['USD', 'EUR'],
                                ['Вернуться']], resize_keyboard=True)


def main_keyboard():
    return ReplyKeyboardMarkup([
                                ['/stoks', 'Валюта', "/crypto"],
                                ['/start']], resize_keyboard=True)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, currency_price))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
    run_scheduler()
