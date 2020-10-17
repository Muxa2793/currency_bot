import dramatiq
import sys
import yfinance as yf
from dramatiq.brokers.redis import RedisBroker
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from db import db, get_financial_asset_db
from datetime import datetime

redis_broker = RedisBroker(host="127.0.0.1", port=6379, db=0)
dramatiq.set_broker(redis_broker)

# dramatiq.Worker(redis_broker)


@dramatiq.actor
def get_financial_asset(financial_asset='USDRUB=X'):
    date = datetime.now()
    price = yf.download(financial_asset, date)['Close'][-1]
    date = date.strftime("%d.%m.%Y %H:%M")
    get_financial_asset_db(db, date, price, financial_asset)


def run_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        get_financial_asset.send,
        CronTrigger.from_crontab("* * * * *"),
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(run_scheduler())
