import os

from PIL import Image, ImageDraw, ImageFont

from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '../Font.ttc'), 13)
FONT_LARGE = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '../Font.ttc'), 24)


class Picture(Observer):

    def __init__(self, observable, filename):
        super().__init__(observable=observable)
        self.filename = filename

    def form_image(self, prices, screen_draw):
        max_price = max(prices)
        min_price = min(prices)
        middle_price = (max_price - min_price) / 2 + min_price

        Plot.line(prices, size=(SCREEN_WIDTH - 45, 93), position=(45, 0), draw=screen_draw)
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

    def update(self, data):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.form_image(data, ImageDraw.Draw(image))
        image.save(self.filename)

    def close(self):
        pass


