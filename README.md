# Проект currency_bot

currency_bot - это бот для Telegram, предназначенный для отображения курса валют.

## Установка

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные:
```
API_KEY = "API-ключ бота"
PROXY_URL = "Адрес прокси"
PROXY_USERNAME = "Логин на прокси"
PROXY_PASSWORD = "Пароль на прокси"

CURRENCY_LIST = ['USD', 'EUR', 'JPY', 'GBP', 'CNY']       # список валют можно изменить и взять с сайта https://finance.yahoo.com
STOCKS_LIST = ['MSFT', 'YNDX', 'TSLA', 'INTC', 'SBER.ME'] # список акций можно изменить и взять с сайта https://finance.yahoo.com
```

6. Запустите бота командой `python3 bot.py`
