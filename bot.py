import logging
import settings

from conv_handlers import USER_SETTINGS, CURRENCY_DB, STOCKS_DB, CRYPTO_DB
from handlers import greet_user, add_notifications_settings
from jobs import get_financial_assets, send_notifications
from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    jq = mybot.job_queue
    jq.run_repeating(get_financial_assets, interval=60, first=0)
    jq.run_repeating(send_notifications, interval=5, first=0)

    dp = mybot.dispatcher

    USER_SETTINGS
    CURRENCY_DB
    STOCKS_DB
    CRYPTO_DB

    dp.add_handler(USER_SETTINGS)
    dp.add_handler(CURRENCY_DB)
    dp.add_handler(STOCKS_DB)
    dp.add_handler(CRYPTO_DB)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("notice", add_notifications_settings))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
