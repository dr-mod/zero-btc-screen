from waveshare_epd import epd2in13_V2
import urllib.request
from urllib.error import HTTPError
import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone, timedelta
import json

SCREEN_HEIGHT = epd2in13_V2.EPD_WIDTH  # 122
SCREEN_WIDTH = epd2in13_V2.EPD_HEIGHT  # 250
REFRESH_INTERVAL = 60 * 15

FONT_SMALL = ImageFont.truetype('Font.ttc', 13)
FONT_LARGE = ImageFont.truetype('Font.ttc', 24)


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


def generate_plot_data(plot, width=200, height=100, displacement=(0, 0)):
    plot_data = []
    for i, element in enumerate(plot):
        x = i * (width / len(plot)) + displacement[0]
        y = height - (element * height) + displacement[1]
        plot_data.append((x, y))
    return plot_data


def form_image(prices, screen_draw):
    screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
    max_price = max(prices)
    min_price = min(prices)
    middle_price = (max_price - min_price) / 2 + min_price
    normalised_data = [(price - min_price) / (max_price - min_price) for price in prices]
    graph_plot = generate_plot_data(normalised_data, width=SCREEN_WIDTH - 45, height=93,
                                    displacement=(45, 0))
    screen_draw.line(graph_plot)
    screen_draw.text((0, -4), "%d" % max_price, font=FONT_SMALL)
    screen_draw.text((0, 39), "%d" % middle_price, font=FONT_SMALL)
    screen_draw.text((0, 81), "%d" % min_price, font=FONT_SMALL)
    screen_draw.line([(10, 98), (240, 98)])
    screen_draw.line([(39, 4), (39, 94)])
    current_price = prices[len(prices) - 1]
    price_text = "BTC = %.2f" % current_price
    text_width, _ = screen_draw.textsize(price_text, FONT_LARGE)
    price_position = ((SCREEN_WIDTH - text_width) / 2, 98)
    screen_draw.text(price_position, price_text, font=FONT_LARGE)


def main():
    try:
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        screen_draw = ImageDraw.Draw(screen_image)
        epd.displayPartBaseImage(epd.getbuffer(screen_image))
        epd.init(epd.PART_UPDATE)

        while True:
            try:
                prices = fetch_prices()
                form_image(prices, screen_draw)

                screen_image_rotated = screen_image.rotate(180)
                epd.displayPartial(epd.getbuffer(screen_image_rotated))
                # TODO: add a way to switch bewen partial and full update
                # epd.display(epd.getbuffer(screen_image_rotated))

                time.sleep(REFRESH_INTERVAL)
            except HTTPError as e:
                print(e)
                time.sleep(5)

        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        epd.sleep()
        epd.Dev_exit()

    except IOError as e:
        print(e)

    except KeyboardInterrupt:
        print("exiting")
        epd2in13_V2.epdconfig.module_exit()
        exit()


if __name__ == "__main__":
    main()

