import datetime
import logging
import settings
from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
  logging.info('Вызван /start')
  update.message.reply_text(
    'Привет, пользователь! Ты вызвал команду /start.\n'
    'Это бот, который покажет интересующие тебя курсы валют, акций и криптовалют.\n'
    'Также в нём скоро появятся другие крутые фишки.'
  )

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
