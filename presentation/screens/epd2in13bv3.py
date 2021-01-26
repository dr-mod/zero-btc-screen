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
    os.path.join(os.path.dirname(__file__), os.pardir, 'Font.ttc'), FONT_SMALL_SIZE)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Font.ttc'), FONT_LARGE_SIZE)


class Epd2in13bv3(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = epd2in13b_V3.EPD()

        self.epd.init()
        self.image_black = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.image_ry = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.draw_black = ImageDraw.Draw(self.image_black)
        self.draw_ry = ImageDraw.Draw(self.image_ry)

    def form_image(self, data):
        self.draw_black.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="white")
        # self.draw_ry.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="white")

        draw_for_data = self.draw_black
        text_fill = "black"
        line_fill = "black"
        graph_fill = "black"

        max_price = max(data)
        min_price = min(data)
        middle_price = (max_price - min_price) / 2 + min_price

        max_price_with, _ = draw_for_data.textsize("%d" % max_price, FONT_SMALL)

        _x_delta = 10
        _x_padding = 4
        _y_delta = 4
        _y_horizontal_line = SCREEN_HEIGHT - FONT_LARGE_SIZE
        _x_sidebar_width = max_price_with + _x_padding

        Plot.line(
            data,
            size=(SCREEN_WIDTH - _x_sidebar_width + _x_padding,
                  _y_horizontal_line - _y_delta),
            position=(_x_sidebar_width + _x_padding, 0),
            draw=draw_for_data,
            fill=graph_fill,
        )

        draw_for_data.text((0, -3), "%d" % max_price, font=FONT_SMALL, fill=text_fill)
        draw_for_data.text((0, (_y_horizontal_line - FONT_SMALL_SIZE) / 2 - _y_delta),
                           "%d" % middle_price, font=FONT_SMALL, fill=text_fill)
        draw_for_data.text((0, _y_horizontal_line - FONT_SMALL_SIZE - _y_delta),
                           "%d" % min_price, font=FONT_SMALL)
        draw_for_data.line([(_x_delta, _y_horizontal_line),
                            (SCREEN_WIDTH - _x_delta, _y_horizontal_line)],
                           fill=line_fill)
        draw_for_data.line([(_x_sidebar_width, _y_delta),
                            (_x_sidebar_width, _y_horizontal_line - _y_delta)],
                           fill=line_fill)

        current_price = data[len(data) - 1]
        price_text = "BTC = %.2f" % current_price
        text_width, _ = draw_for_data.textsize(price_text, FONT_LARGE)
        price_position = ((SCREEN_WIDTH - text_width) / 2, SCREEN_HEIGHT - FONT_LARGE_SIZE)
        draw_for_data.text(price_position, price_text, font=FONT_LARGE, fill=text_fill)

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
