import logging
import settings

from handlers import greet_user, get_currency_price, get_stocks_price, choose_currency, choose_stocks, currency_db_dontknow, add_notifications_settings
from jobs import get_financial_assets#, send_notifications
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from user_settings import user_settings_start, user_settings_dontknow, user_settings_currency, user_settings_stocks, user_settings_set_asset

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
                                'username': settings.PROXY_USERNAME,
                                'password': settings.PROXY_PASSWORD}}

logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%d-%m-%y %H:%M:%S')


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    jq = mybot.job_queue
    jq.run_repeating(get_financial_assets, interval=60, first=0)
    #jq.run_repeating(send_notifications, interval=5, first=0)

    dp = mybot.dispatcher

    user_settings = ConversationHandler(
        entry_points=[
            CommandHandler('settings', user_settings_start)
        ],
        states={
            'set_asset': [MessageHandler(Filters.text, user_settings_set_asset)], 
            'currency': [CallbackQueryHandler(user_settings_currency)],
            'stocks': [CallbackQueryHandler(user_settings_stocks)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                           user_settings_dontknow)
        ]
    )

    stocks_db = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Акции)$'), choose_stocks)
        ],
        states={
            'stocks_price': [MessageHandler(Filters.text, get_stocks_price)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                           currency_db_dontknow)
        ]
    )

    currency_db = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Валюта)$'), choose_currency)
        ],
        states={
            'currency_price': [MessageHandler(Filters.text, get_currency_price)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                           currency_db_dontknow)
        ]
    )

    dp.add_handler(user_settings)
    dp.add_handler(currency_db)
    dp.add_handler(stocks_db)
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("notice", add_notifications_settings))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
