import os

from PIL import ImageFont

from data.plot import Plot

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'Roses.ttf'), 8)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Default:

    def __init__(self, width, mode):
        self.width = width
        self.mode = mode

    def form_image(self, image_draw, prices):
        if self.mode == "candle":
            Plot.candle(prices, size=(self.width - 45, 93), position=(41, 0), draw=image_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(self.width - 42, 93), position=(42, 0), draw=image_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, 89), draw=image_draw)
        image_draw.line([(10, 98), (240, 98)])
        image_draw.line([(39, 4), (39, 94)])
        image_draw.line([(60, 102), (60, 119)])
        Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, self.width, FONT_LARGE, image_draw)