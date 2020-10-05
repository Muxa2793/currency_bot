import datetime
import logging
import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from datetime import datetime, date, time
import yfinance as yf
import pandas

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
    logging.info('Вызван /start')
    my_keyboard = ReplyKeyboardMarkup([
                                        ['/stoks', '/currency', "/crypto"],
                                        ['/start']
                                        ])
    update.message.reply_text(
      'Привет, пользователь! Ты вызвал команду /start.\n'
      'Это бот, который покажет интересующие тебя курсы валют, акций и криптовалют.\n'
      'Также в нём скоро появятся другие крутые фишки.', reply_markup = my_keyboard
    )
    

def currency_price(update,context):
    pass 

def stoks_price(update,context):
    user_text = update.message.text
    price = yf.download(user_text, datetime.now().date())['Close'][0]
    price = round(price, 2)
    update.message.reply_text(f'{user_text}: {price}$')

def cryptocurrency_price(update,context):
    pass

def stoks_price_command(update, context):
    print('Вызвана команда /stoks')
    my_keyboard = ReplyKeyboardMarkup([
                                        ['YNDX', 'TSLA', 'MSFT', 'USDRUB=X'],
                                        ['/start']
                                        ])
    if update.message.text == '/stoks':
        update.message.reply_text('Выберите бумагу', reply_markup = my_keyboard)
    if update.message.text == 'YNDX' or  update.message.text == 'TSLA' or update.message.text == 'MSFT' or update.message.text == 'USDRUB=X':
        stoks_price(update,context)
    

def currency_price_command(update,context):
    pass

def cryptocurrency_price_command(update,context):
    pass

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("currency", currency_price_command))
    dp.add_handler(CommandHandler("stoks", stoks_price_command))
    dp.add_handler(CommandHandler("crypto", cryptocurrency_price_command))
    dp.add_handler(MessageHandler(Filters.text, stoks_price_command))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
