import os

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13b_V3

from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = epd2in13b_V3.EPD_WIDTH  # 104
SCREEN_WIDTH = epd2in13b_V3.EPD_HEIGHT  # 212

FONT_SMALL_SIZE = 12
FONT_LARGE_SIZE = 24
FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), '../Font.ttc'), FONT_SMALL_SIZE)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), '../Font.ttc'), FONT_LARGE_SIZE)


class Epd2in13bV3(Observer):

    def __init__(self, observable):
        super().__init__(observable=observable)
        self.epd = epd2in13b_V3.EPD()

        self.epd.init()
        self.epd.Clear()
        self.image_black = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.image_ry = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.draw_black = ImageDraw.Draw(self.image_black)
        self.draw_ry = ImageDraw.Draw(self.image_ry)

    def form_image(self, data):
        # self.draw_black.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        max_price = max(data)
        min_price = min(data)
        middle_price = (max_price - min_price) / 2 + min_price

        _x_delta = 10
        _y_delta = 4
        _y_horizontal_line = SCREEN_HEIGHT - FONT_LARGE_SIZE

        Plot.line(data, size=(SCREEN_WIDTH - 45, _y_horizontal_line - _y_delta), position=(45, 0), draw=self.draw_black)

        self.draw_black.text((0, -3), "%d" % max_price, font=FONT_SMALL)
        self.draw_black.text((0, (_y_horizontal_line - FONT_SMALL_SIZE) / 2 - _y_delta),
                             "%d" % middle_price, font=FONT_SMALL)
        self.draw_black.text((0, _y_horizontal_line - FONT_SMALL_SIZE - _y_delta),
                             "%d" % min_price, font=FONT_SMALL)
        self.draw_black.line([(_x_delta, _y_horizontal_line),
                              (SCREEN_WIDTH - _x_delta, _y_horizontal_line)])
        # TODO: calculate 39 from max of (max, middle, min prices)
        self.draw_black.line([(39, _y_delta), (39, _y_horizontal_line - _y_delta)])

        current_price = data[len(data) - 1]
        price_text = "BTC = %.2f" % current_price
        text_width, _ = self.draw_black.textsize(price_text, FONT_LARGE)
        price_position = ((SCREEN_WIDTH - text_width) / 2, SCREEN_HEIGHT - FONT_LARGE_SIZE)
        self.draw_black.text(price_position, price_text, font=FONT_LARGE)

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
