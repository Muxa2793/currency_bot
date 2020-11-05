# Проект currency_bot

currency_bot - это бот для Telegram, предназначенный для отображения курса валют и акций.

## Установка

1. Создайте нового бота. Инструкция по созданию бота с помощью [BotFather](https://medium.com/@bbsystemscorporation/инструкция-по-работе-с-botfather-ботом-5c6f74d99a1a)
2. Клонируйте репозиторий с github
3. Создайте виртуальное окружение
4. Установите зависимости `pip install -r requirements.txt`
5. Создайте файл `settings.py`
6. Впишите в settings.py переменные:
```
API_KEY = "API-ключ бота"
PROXY_URL = "Адрес прокси"
PROXY_USERNAME = "Логин на прокси"
PROXY_PASSWORD = "Пароль на прокси"

CURRENCY_LIST = ['USD', 'EUR', 'JPY', 'GBP', 'CNY']       # список валют можно изменить и взять с сайта https://finance.yahoo.com
STOCKS_LIST = ['MSFT', 'YNDX', 'TSLA', 'INTC', 'SBER.ME'] # список акций можно изменить и взять с сайта https://finance.yahoo.com
```

7. Запустите бота командой `python3 bot.py`
8. Найдите бота в telegram и Напишите команду `/start`
