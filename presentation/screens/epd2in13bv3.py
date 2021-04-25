from PIL import Image, ImageDraw
from waveshare_epd import epd2in13b_V3

from presentation.observer import Observer
from presentation.screens.layouts.default import Default

SCREEN_HEIGHT = epd2in13b_V3.EPD_WIDTH  # 104
SCREEN_WIDTH = epd2in13b_V3.EPD_HEIGHT  # 212


class Epd2in13bv3(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = epd2in13b_V3.EPD()

        self.epd.init()
        self.image_black = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.image_ry = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.draw_black = ImageDraw.Draw(self.image_black)
        self.draw_ry = ImageDraw.Draw(self.image_ry)
        self.layout = Default(SCREEN_WIDTH, mode)

    def form_image(self, prices):
        self.draw_black.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="white")
        self.layout.form_image(self.draw_black, prices)

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
