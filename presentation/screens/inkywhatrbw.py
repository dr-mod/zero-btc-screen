import os

from inky import InkyWHAT

from PIL import Image, ImageDraw, ImageFont

from data.plot import Plot
from presentation.observer import Observer

inky_display = InkyWHAT("black")
#inky_display.set_border(inky_display.WHITE)

SCREEN_HEIGHT = inky_display.WIDTH  # 400
SCREEN_WIDTH = inky_display.HEIGHT  # 300

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Inkywhatrbw(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.mode = mode

    def form_image(self, prices):
        screen_draw = ImageDraw.Draw(self.image)
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="white")
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 38, 79), position=(35, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 36, 79), position=(36, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        screen_draw.line([(60, 102), (60, 119)])
        Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, data):
        self.form_image(data)
        inky_display.set_image(self.image)
        inky_display.show()

    def close(self):
        pass
