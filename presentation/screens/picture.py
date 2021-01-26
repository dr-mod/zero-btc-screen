import os

from PIL import Image, ImageDraw, ImageFont

from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Font.ttc'), 13)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Font.ttc'), 24)


class Picture(Observer):

    def __init__(self, observable, filename):
        super().__init__(observable=observable)
        self.filename = filename

    def form_image(self, prices, screen_draw):
        Plot.line(prices, size=(SCREEN_WIDTH - 45, 93), position=(45, 0), draw=screen_draw)
        Plot.y_axis_labels(prices, FONT_SMALL, (0, -4), (0, 81), draw=screen_draw)
        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        Plot.caption(prices[len(prices) - 1], 98, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, data):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.form_image(data, ImageDraw.Draw(image))
        image.save(self.filename)

    def close(self):
        pass


