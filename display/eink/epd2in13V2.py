import os

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V2

from data.plot import Plot
from display.observer import Observer

SCREEN_HEIGHT = epd2in13_V2.EPD_WIDTH  # 122
SCREEN_WIDTH = epd2in13_V2.EPD_HEIGHT  # 250

FONT_SMALL = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '../Font.ttc'), 13)
FONT_LARGE = ImageFont.truetype(os.path.join(os.path.dirname(__file__), '../Font.ttc'), 24)


class Epd2in13V2(Observer):

    def __init__(self, observable):
        super().__init__(observable=observable)
        self.epd = epd2in13_V2.EPD()
        self.screen_image = self._init_display(self.epd)

    @staticmethod
    def _init_display(epd):
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        epd.displayPartBaseImage(epd.getbuffer(screen_image))
        epd.init(epd.PART_UPDATE)
        return screen_image

    # TODO: Data normalisation should be externalised
    def form_image(self, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
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
        self.form_image(data, ImageDraw.Draw(self.screen_image))
        screen_image_rotated = self.screen_image.rotate(180)
        # TODO: add a way to switch bewen partial and full update
        # epd.display(epd.getbuffer(screen_image_rotated))
        self.epd.displayPartial(self.epd.getbuffer(screen_image_rotated))

    @staticmethod
    def close():
        epd2in13_V2.epdconfig.module_exit()
