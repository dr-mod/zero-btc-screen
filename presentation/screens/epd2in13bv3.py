import os

from PIL import Image, ImageDraw, ImageFont
try:
    from waveshare_epd import epd2in13b_V3
except ImportError:
    pass
from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 104
SCREEN_WIDTH = 212

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 7)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 22)

class Epd2in13bv3(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = epd2in13b_V3.EPD()

        self.epd.init()
        self.image_black = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.image_ry = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.draw_black = ImageDraw.Draw(self.image_black)
        self.draw_ry = ImageDraw.Draw(self.image_ry)
        self.mode = mode

    def form_image(self, prices):
        self.draw_black.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="white")
        screen_draw = self.draw_black
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 38, 79), position=(35, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 36, 79), position=(36, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (32, 76), draw=screen_draw)
        screen_draw.line([(9, 83), (204, 83)])
        screen_draw.line([(33, 3), (33, 80)])
        screen_draw.line([(51, 87), (51, 101)])
        Plot.caption(flatten_prices[len(flatten_prices) - 1], 81, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, data):
        self.form_image(data)
        image_black_rotated = self.image_black.rotate(180)
        image_ry_rotated = self.image_ry.rotate(180)
        self.epd.display(
            self.epd.getbuffer(image_black_rotated),
            self.epd.getbuffer(image_ry_rotated)
        )

    def close(self):
        self.epd.Dev_exit()
