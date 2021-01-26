import json
import random
import time
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable

DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
API_URL = 'https://production.api.coindesk.com/v2/price/values/BTC?ohlc=false'


def get_dummy_data():
    logger.info('Generating dummy data')
    random.seed(1)
    return [random.randint(9999, 99000) for _ in range(0, 97)]


def fetch_prices():
    logger.info('Fetching prices')
    timeslot_end = datetime.now(timezone.utc)
    end_date = timeslot_end.strftime(DATETIME_FORMAT)
    start_data = (timeslot_end - timedelta(days=DATA_SLICE_DAYS)).strftime(DATETIME_FORMAT)
    url = f'{API_URL}&start_date={start_data}&end_date={end_date}'
    req = Request(url)
    data = urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1] for entry in external_data['data']['entries']]
    return prices


def main():
    logger.info('Initialize')

    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)

    try:
        while True:
            try:
                prices = get_dummy_data() if config.dummy_data else fetch_prices()
                data_sink.update_observers(prices)
                time.sleep(config.refresh_interval)
            except (HTTPError, URLError) as e:
                logger.error(str(e))
                time.sleep(5)
    except IOError as e:
        logger.error(str(e))
    except KeyboardInterrupt:
        logger.info('Exit')
        data_sink.close()
        exit()


if __name__ == "__main__":
    main()
