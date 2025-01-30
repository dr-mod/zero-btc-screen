import math
from config.config import config

class Plot:
    @staticmethod
    def line(prices, size=(100, 100), position=(0, 0), draw=None, fill=None):
        assert draw
        max_price = max(prices)
        min_price = min(prices)
        normalised_prices = [(price - min_price) / (max_price - min_price) for price in prices]
        plot_data = []
        for i, element in enumerate(normalised_prices):
            x = i * (size[0] / len(normalised_prices)) + position[0]
            y = size[1] - (element * size[1]) + position[1]
            plot_data.append((x, y))
        draw.line(plot_data, fill=fill)

    @staticmethod
    def y_axis_labels(prices, font, position_first=(0, 0), position_last=(0, 0), draw=None, fill=None, labels_number=3):
        def center_x(price):
            area_width = position_last[0] - position_first[0]
            text_width = draw.textlength(price, font)
            if area_width >= text_width:
                return position_first[0] + (area_width - text_width) / 2
            else:
                return position_first[0]

        max_price = max(prices)
        min_price = min(prices)
        price_step = (max_price - min_price) / (labels_number - 1)
        y_step = (position_last[1] - position_first[1]) / (labels_number - 1)
        for i in range(0, labels_number):
            human_price = Plot.human_format(min_price + i * price_step, 5)
            draw.text((center_x(human_price), position_last[1] - i * y_step), human_price, font=font, fill=fill)

    @staticmethod
    def percentage(prices, x_middle, y, font, draw, fill=None):
        open = prices[0][0]
        close = prices[len(prices) - 1][3]
        percentage = ((1 - (close / open)) * -1) * 100

        price_text = Plot.human_format(percentage, 4, 0)
        price_text = price_text + "%"
        if percentage > 0:
            price_text = "+" + price_text
        text_width, _ = draw.textsize(price_text, font)
        price_position = ((x_middle - (text_width / 2)), y)
        draw.text(price_position, price_text, font=font, fill=fill)
        return text_width

    @staticmethod
    def caption(price, y, screen_width, font, draw, fill=None, currency_offset=-1, price_offset=60):
        draw.text((currency_offset, y), config.currency[:3], font=font, fill=fill)
        price_text = Plot.human_format(price, 8, 2)
        text_width = draw.textlength(price_text, font)
        price_position = (((screen_width - text_width - price_offset) / 2) + price_offset, y)
        draw.text(price_position, price_text, font=font, fill=fill)

    @staticmethod
    def candle(data, size=(100, 100), position=(0, 0), draw=None, fill_neg="#000000", fill_pos=None):
        # data[open, high, low, close]
        width = size[0]
        height = size[1]

        candle_width = 9
        space = 1

        num_of_candles = width // (candle_width + space)
        leftover_space = width % (candle_width + space)
        windows_per_candle = len(data) // num_of_candles
        data_offset = len(data) % num_of_candles
        candle_data = []
        for i in range(data_offset, len(data), windows_per_candle):
            window = data[i:i + windows_per_candle]
            open = window[0][0]
            close = window[len(window) - 1][3]
            high = max([i[1] for i in window])
            low = min([i[2] for i in window])
            candle_data.append((open, high, low, close))

        all_values = [item for sublist in candle_data for item in sublist]
        max_price = max(all_values)
        min_price = min(all_values)

        normalised_data = []
        for line in candle_data:
            normalised_line = []
            normalised_data.append(normalised_line)
            for i in range(len(line)):
                price = line[i]
                normalised_line.append((price - min_price) / (max_price - min_price))

        def y_flip(y):
            return height - (y * height) + position[1]

        for i, element in enumerate(normalised_data):
            open = element[0]
            close = element[3]
            high = element[1]
            low = element[2]
            x = candle_width * i + space * i + leftover_space / 2 + position[0]
            # high price
            wick_x = x + (candle_width // 2)
            draw.line([wick_x, y_flip(high), wick_x, y_flip(max(open, close))], fill=fill_pos)
            # low price
            draw.line([wick_x, y_flip(low), wick_x, y_flip(min(open, close))], fill=fill_pos)

            open_y = math.floor(y_flip(open))
            close_y = math.floor(y_flip(close))
            if open_y == close_y:
                draw.line([x, open_y, x + candle_width - 1, close_y], fill=fill_pos)
            else:
                if open < close:
                    # draw.rectangle([x, open_y, x + candle_width - 1, close_y], fill=fill_pos)
                    draw.rectangle([x, close_y, x + candle_width - 1, open_y], fill=fill_pos)
                else:
                    draw.rectangle([x, open_y, x + candle_width - 1, close_y], fill=fill_neg)

    # TODO: Adapt for big numbers 1k, 1m, etc
    @staticmethod
    def human_format(number, length, fractional_minimal=0):
        magnitude = 0
        num = number
        while abs(num) >= 10:
            magnitude += 1
            num /= 10.0
        format_string = f'%.{fractional_minimal}f'
        if length >= magnitude + fractional_minimal + 2:
            fractional_length = length - magnitude - 2
            format_string = f'%.{fractional_length}f'
        return format_string % number
