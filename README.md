# Проект currency_bot

currency_bot - это бот для Telegram, написанны на языке Python и предназначенный для отображения курса валют и акций.

Бот был разработан в качестве дипломного проекта для LearnPython.

## Установка бота

1. Создайте нового бота. Инструкция по созданию бота с помощью [BotFather](https://medium.com/@bbsystemscorporation/инструкция-по-работе-с-botfather-ботом-5c6f74d99a1a)
2. Клонируйте репозиторий с github
3. Создайте виртуальное окружение
4. Установите зависимости `pip install -r requirements.txt`
5. Создайте файл `settings.py`
6. Впишите в settings.py переменные:
```python
API_KEY = "API-ключ бота"
PROXY_URL = "Адрес прокси"
PROXY_USERNAME = "Логин на прокси"
PROXY_PASSWORD = "Пароль на прокси"

CURRENCY_LIST = ['USD', 'EUR', 'JPY', 'GBP', 'CNY']       # список можно изменить на свой
STOCKS_LIST = ['MSFT', 'YNDX', 'TSLA', 'INTC', 'SBER.ME'] # список можно изменить на свой
```
      
   - ***Список доступных валют на [yahoofinance](https://finance.yahoo.com/most-active)***
   - ***Список доступных акций на [yahoofinance](https://finance.yahoo.com/currencies)***

7. Запустите бота командой `python3 bot.py` 

## Настройка базы данных
1. Создайте базу данных в MongoDB
2. Добавьте в `settings.py` переменные:
```python
MONGO_LINK = 'Ссылка на базу данных'
MONGO_DB = 'Название базы данных'
```
## Запуск
1. Найдите вашего бота в telegram и Напишите команду `/start`
