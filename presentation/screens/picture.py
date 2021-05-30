import os

from PIL import Image, ImageDraw, ImageFont

from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Picture(Observer):

    def __init__(self, observable, filename, mode):
        super().__init__(observable=observable)
        self.filename = filename
        self.mode = mode

    def update(self, prices):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        screen_draw = ImageDraw.Draw(image)
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, 93), position=(41, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 42, 93), position=(42, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        screen_draw.line([(60, 102), (60, 119)])
        Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)
        image.save(self.filename)

    def close(self):
        pass
