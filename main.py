from display.observer import Observable
from display.eink.epd2in13V2 import Epd2in13V2
import urllib.request
from urllib.error import HTTPError
import time
from datetime import datetime, timezone, timedelta
import json

REFRESH_INTERVAL = 60 * 15


def fetch_prices():
    timeslot_end = datetime.now(timezone.utc)
    timeslot_start = timeslot_end - timedelta(days=1)
    req = urllib.request.Request("https://production.api.coindesk.com/v2/price/values/BTC?start_date="
                                 "%s&end_date=%s&ohlc=false" % (timeslot_start.strftime("%Y-%m-%dT%H:%M"),
                                                                timeslot_end.strftime("%Y-%m-%dT%H:%M")))
    data = urllib.request.urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1] for entry in external_data['data']['entries']]
    return prices


def main():
    data_sink = Observable()
    Epd2in13V2(data_sink)
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
        exit()


if __name__ == "__main__":
    main()

