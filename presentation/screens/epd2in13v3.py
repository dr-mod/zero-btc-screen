from presentation.screens.epd2in13v2 import Epd2in13v2

try:
    from waveshare_epd import epd2in13_V3
except ImportError:
    pass


class Epd2in13v3(Epd2in13v2):
    @staticmethod
    def _init_display():
        epd = epd2in13_V3.EPD()
        epd.init()
        epd.Clear(0xFF)
        return epd

    def close(self):
        epd2in13_V3.epdconfig.module_exit()


