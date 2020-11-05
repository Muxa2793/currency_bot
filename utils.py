from telegram import ReplyKeyboardMarkup
from db import db, get_user_currency_keyboard


def main_keyboard():
    return ReplyKeyboardMarkup([
                                ['/stoks', 'Валюта', "/crypto"],
                                ['/start', '/settings']], resize_keyboard=True)


def assets_keyboard():
    return ReplyKeyboardMarkup([
                                ['Валюта', 'Акции', "Криптовалюта", "Выйти"]], resize_keyboard=True)


def user_currency_keyboard(update):
    keyboard = get_user_currency_keyboard(db, update.effective_user)
    return ReplyKeyboardMarkup([
                                keyboard,
                                ['Вернуться']], resize_keyboard=True)
