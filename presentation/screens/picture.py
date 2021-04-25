from PIL import Image, ImageDraw

from presentation.observer import Observer
from presentation.screens.layouts.default import Default

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250


class Picture(Observer):

    def __init__(self, observable, filename, mode):
        super().__init__(observable=observable)
        self.filename = filename
        self.layout = Default(SCREEN_WIDTH, mode)

    def update(self, data):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.layout.form_image(ImageDraw.Draw(image), data)
        image.save(self.filename)

    def close(self):
        pass

