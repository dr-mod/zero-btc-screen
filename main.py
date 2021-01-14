import json
import os
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError

from display import eink
from display.observer import Observable

REFRESH_INTERVAL = 60 * 15
DATA_SLICE_DAYS = 1
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"
API_URL = 'https://production.api.coindesk.com/v2/price/values/BTC?ohlc=false'


def fetch_prices():
    timeslot_end = datetime.now(timezone.utc)
    end_date = timeslot_end.strftime(DATETIME_FORMAT)
    start_data = (timeslot_end - timedelta(days=DATA_SLICE_DAYS)).strftime(DATETIME_FORMAT)
    url = f'{API_URL}&start_date={start_data}&end_date={end_date}'
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1] for entry in external_data['data']['entries']]
    return prices


def main():
    data_sink = Observable()

    eink_driver_name = os.environ.get('BTC_SCREEN_DRIVER', 'epd2in13_V2').replace('_', '')
    # we do not want to lowercase the rest
    eink_class_name = eink_driver_name[0].capitalize() + eink_driver_name[1:]
    try:
        driver = getattr(eink, eink_driver_name)
        getattr(driver, eink_class_name)(data_sink)
    except AttributeError:
        raise BtcConfigError(
            f'I can not initialize a drive with a provided name {eink_driver_name}')

    try:
        while True:
            try:
                prices = fetch_prices()
                data_sink.update_observers(prices)
                time.sleep(REFRESH_INTERVAL)
            except HTTPError as e:
                print(e)
                time.sleep(5)
    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        print("exiting")
        data_sink.close()
        exit()


class BtcConfigError(Exception):
    """Custom BTC screen Exception"""


if __name__ == "__main__":
    main()
