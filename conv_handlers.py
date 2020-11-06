from handlers import get_currency_price, choose_currency, currency_db_dontknow
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from user_settings import user_settings_start, user_settings_dontknow, user_settings_currency, user_settings_set_asset

USER_SETTINGS = ConversationHandler(
    entry_points=[
        CommandHandler('settings', user_settings_start)
    ],
    states={
        'set_asset': [MessageHandler(Filters.text, user_settings_set_asset)],
        'currency': [CallbackQueryHandler(user_settings_currency)]
    },
    fallbacks=[
        MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.location | Filters.document,
                       user_settings_dontknow)
    ]
)

CURRENCY_DB = ConversationHandler(
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
