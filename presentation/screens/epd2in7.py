import os

from PIL import Image, ImageDraw, ImageFont
try:
    from waveshare_epd import epd2in7
except ImportError:
    pass
from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 176
SCREEN_WIDTH = 264

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 10)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 27)

class Epd2in7v1(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = self._init_display()
        self.screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.screen_draw = ImageDraw.Draw(self.screen_image)
        self.mode = mode

    @staticmethod
    def _init_display():
        epd = epd2in7.EPD()
        epd.init()
        epd.Clear(0xFF)
        return epd

    def form_image(self, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        screen_draw = self.screen_draw
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, 126), position=(41, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 45, 126), position=(42, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (2, 8), (38, 112), draw=screen_draw)
        screen_draw.line([(9, 130), (255, 130)])
        screen_draw.line([(41, 4), (41, 126)])
        Plot.caption(flatten_prices[len(flatten_prices) - 1], 139, SCREEN_WIDTH, FONT_LARGE, screen_draw, None, 12, 64)

    def update(self, data):
        self.form_image(data, self.screen_draw)
        screen_image_rotated = self.screen_image.rotate(180)
        self.epd.display(self.epd.getbuffer(screen_image_rotated))

    def close(self):
        epd2in7.epdconfig.module_exit()
