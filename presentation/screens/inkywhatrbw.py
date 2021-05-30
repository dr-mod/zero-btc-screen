import os

from inky import InkyWHAT

from PIL import Image, ImageDraw, ImageFont

from data.plot import Plot
from presentation.observer import Observer

inky_display = InkyWHAT("red")
inky_display.set_border(inky_display.WHITE)

SCREEN_WIDTH = inky_display.WIDTH # 400
SCREEN_HEIGHT = inky_display.HEIGHT  # 300

LEFT_MARGIN = 55
BOTTOM_MARGIN = 30

SMALL_FONT_SIZE = 10
FONT_SMALL = ImageFont.truetype(os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), SMALL_FONT_SIZE)

LARGE_FONT_SIZE = 26
FONT_LARGE = ImageFont.truetype(os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), LARGE_FONT_SIZE)

class Inkywhatrbw(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.image = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mode = mode

    def form_image(self, prices):
        screen_draw = ImageDraw.Draw(self.image)
        screen_draw.rectangle([0,0,SCREEN_WIDTH,SCREEN_HEIGHT],fill=inky_display.WHITE)
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - LEFT_MARGIN, SCREEN_HEIGHT - BOTTOM_MARGIN), position=(LEFT_MARGIN, 0), draw=screen_draw, fill_neg=inky_display.RED, fill_pos=inky_display.BLACK)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - LEFT_MARGIN, SCREEN_HEIGHT - BOTTOM_MARGIN), position=(LEFT_MARGIN, 0), draw=screen_draw, fill=inky_display.BLACK)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (LEFT_MARGIN, SCREEN_HEIGHT - BOTTOM_MARGIN - SMALL_FONT_SIZE - 3), draw=screen_draw, fill=inky_display.BLACK)
        screen_draw.line([(0, SCREEN_HEIGHT - BOTTOM_MARGIN), (SCREEN_WIDTH, SCREEN_HEIGHT - BOTTOM_MARGIN)], fill=inky_display.BLACK)
        screen_draw.line([(LEFT_MARGIN, 0), (LEFT_MARGIN, SCREEN_HEIGHT - BOTTOM_MARGIN)], fill=inky_display.BLACK)
        #screen_draw.line([(LEFT_MARGIN * 4, SCREEN_HEIGHT - BOTTOM_MARGIN), (LEFT_MARGIN * 4, SCREEN_HEIGHT)], fill=inky_display.BLACK)
        Plot.caption(flatten_prices[len(flatten_prices) - 1], SCREEN_HEIGHT - BOTTOM_MARGIN, SCREEN_WIDTH, FONT_LARGE, screen_draw, fill=inky_display.BLACK, currency_offset=LEFT_MARGIN, price_offset=LEFT_MARGIN)

    def update(self, data):
        self.form_image(data)
        inky_display.set_image(self.image)
        inky_display.show()

    def close(self):
        pass
