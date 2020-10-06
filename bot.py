import logging
import settings
import yfinance as yf
from datetime import datetime, date, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
    logging.info('Вызван /start')
    my_keyboard = ReplyKeyboardMarkup([
                                        ['/stoks', 'Валюта', "/crypto"],
                                        ['/start']
                                        ], resize_keyboard=True)
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют, акций и криптовалют.\n'
      'Также в нём скоро появятся другие крутые фишки.', reply_markup = my_keyboard
    )
    
def currency_price_command(update,context):
    if update.message.text == 'Валюта':
        update.message.reply_text('Выберите валюту', reply_markup = currency_keyboard())
    if update.message.text == 'USD' or  update.message.text == 'EUR':
        print(update.message.text)
        update.message.reply_text(f'{update.message.text}: {currency_price(update.message.text)}$')

def currency_price(currency):
    if currency == 'USD':
        current_currency = 'USDRUB=X'
        price = yf.download(current_currency, datetime.now().date())['Close'][0]
        price = round(price, 2)
        return price

def currency_keyboard():
    return ReplyKeyboardMarkup([
                                ['USD', 'EUR'],
                                ['Вернуться']
                                ], resize_keyboard=True)

def main_keyboard(update, context):
    keyboard =  ReplyKeyboardMarkup([
                                    ['/stoks', 'Валюта', "/crypto"],
                                    ['/start']
                                    ], resize_keyboard=True)
    update.message.reply_text('Выберете то, что вас интересует', reply_markup = keyboard)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, currency_price_command))
    dp.add_handler(MessageHandler(Filters.regex('^(Валюта)$'), currency_price_command))
    dp.add_handler(MessageHandler(Filters.regex('^(Вернуться)$'), main_keyboard), group=1)
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
