import os

from PIL import Image, ImageDraw, ImageFont
try:
    from waveshare_epd import epd3in7
except ImportError:
    pass
from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 280
SCREEN_WIDTH = 480

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)


class Epd3in7(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = self._init_display()
        self.screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.screen_draw = ImageDraw.Draw(self.screen_image)
        self.mode = mode

    @staticmethod
    def _init_display():
        epd = epd3in7.EPD()
        epd.init(0)
        epd.Clear(0xFF, 0)
        epd.init(1)
        epd.Clear(0xFF, 1)
        return epd

    def form_image(self, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, SCREEN_HEIGHT - 27), position=(41, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 42, SCREEN_HEIGHT - 27), position=(42, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, SCREEN_HEIGHT - 34), draw=screen_draw,
                           labels_number=5)
        screen_draw.line([(10, SCREEN_HEIGHT - 25), (470, SCREEN_HEIGHT - 25)])
        screen_draw.line([(39, 4), (39, SCREEN_HEIGHT - 27)])
        screen_draw.line([(60, SCREEN_HEIGHT - 23), (60, SCREEN_HEIGHT - 1)])
        # screen_draw.text((-1, SCREEN_HEIGHT - 27), "XXX"[:3], font=FONT_LARGE, fill=None)
        Plot.caption(flatten_prices[len(flatten_prices) - 1], SCREEN_HEIGHT - 27, SCREEN_WIDTH - 45, FONT_LARGE, screen_draw,
                     price_offset=0)
        Plot.percentage(prices, SCREEN_WIDTH - 56, SCREEN_HEIGHT - 27, FONT_LARGE, screen_draw)

        screen_draw.line([(366, SCREEN_HEIGHT - 23), (366, SCREEN_HEIGHT - 1)])

    def update(self, data):
        self.form_image(data, self.screen_draw)
        screen_image_rotated = self.screen_image.rotate(180)
        self.epd.display_1Gray(self.epd.getbuffer(screen_image_rotated))

    def close(self):
        epd3in7.epdconfig.module_exit()
