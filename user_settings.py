import logging
from db import db, get_or_create_user, create_currency_list
from settings import CURRENCY_LIST
from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from utils import assets_keyboard, main_keyboard


def user_settings_start(update, context):
    logging.info('Вызван /settings')

    get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Привет пользователь! Давай настроим твоего бота. Выбери актив, который '
                              'ты хочешь настроить', reply_markup=assets_keyboard())
    return 'set_asset'


def user_settings_set_asset(update, context):
    user_text = update.message.text
    if user_text == 'Валюта':
        keyboard = [
            [
                InlineKeyboardButton("USD", callback_data='USD'),
                InlineKeyboardButton("EUR", callback_data='EUR')
            ],
            [
                InlineKeyboardButton("JPY", callback_data='JPY'),
                InlineKeyboardButton("GBP", callback_data='GBP')
            ],
            [
                InlineKeyboardButton("CNY", callback_data='CNY'),
                InlineKeyboardButton("Закончить", callback_data='Закончить')
            ]
        ]
        currency_keyboard = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберете валюту или нажмите закончить', reply_markup=currency_keyboard)
        context.user_data['currency'] = []
        user_text = update.message.text
        return 'currency'
    elif user_text == 'Акции':
        update.message.reply_text('Вы выбрали акции')
    elif user_text == 'Выйти':
        update.message.reply_text("Настройка завершена", reply_markup=main_keyboard())
        return ConversationHandler.END


def user_settings_currency(update, context):
    query = update.callback_query
    query.answer()
    if query.data not in context.user_data['currency']:
        if query.data in CURRENCY_LIST:
            context.user_data['currency'].append(query.data)
            query.message.reply_text(f"Валюта {query.data} добавлена в ваш список валют",
                                     reply_markup=ReplyKeyboardRemove())
            user_currency_list = context.user_data['currency']
            create_currency_list(db, update.effective_user, user_currency_list)
        elif query.data == 'Закончить':
            if context.user_data['currency'] == []:
                query.message.reply_text("Вы не добавили ни одной валюты, пожалуйста выберите валюту",
                                         reply_markup=ReplyKeyboardRemove())
            else:
                query.message.reply_text("Настройка завершена", reply_markup=assets_keyboard())
                return 'set_asset'
    else:
        query.message.reply_text(f"Валюта {query.data} уже есть в списке, выберете другую")


def user_settings_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
