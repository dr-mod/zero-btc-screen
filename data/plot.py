import math


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

    # TODO: Implement variable number of elements to generate
    @staticmethod
    def y_axis_labels(prices, font, position_first=(0, 0), position_last=(0, 0), draw=None):
        def center_x(price):
            area_width = position_last[0] - position_first[0]
            text_width, _ = draw.textsize(price, font)
            if area_width >= text_width:
                return position_first[0] + (area_width - text_width) / 2
            else:
                return position_first[0]

        max_price = max(prices)
        min_price = min(prices)
        middle_price = (max_price - min_price) / 2 + min_price

        price = "%d" % max_price
        draw.text((center_x(price), position_first[1]), price, font=font)
        price = "%d" % middle_price
        draw.text((center_x(price), (position_last[1] - position_first[1]) / 2 + position_first[1]), price, font=font)
        price = "%d" % min_price
        draw.text((center_x(price), position_last[1]), price, font=font)

    @staticmethod
    def caption(price, y, screen_width, font, draw):
        draw.text((-1, y), "BTC", font=font)
        price_text = "%.2f" % price
        text_width, _ = draw.textsize(price_text, font)
        price_position = (((screen_width - text_width - 60) / 2) + 60, y)
        draw.text(price_position, price_text, font=font)

    @staticmethod
    def candle(data, size=(100, 100), position=(0, 0), draw=None):
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
            window = data[i:i + windows_per_candle - 1]
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
            draw.line([wick_x, y_flip(high), wick_x, y_flip(max(open, close))])
            # low price
            draw.line([wick_x, y_flip(low), wick_x, y_flip(min(open, close))])

            open_y = math.floor(y_flip(open))
            close_y = math.floor(y_flip(close))
            if open_y == close_y:
                draw.line([x, open_y, x + candle_width - 1, close_y])
            elif open_y < close_y:
                draw.rectangle([x, open_y, x + candle_width - 1, close_y])
            else:
                draw.rectangle([x, open_y, x + candle_width - 1, close_y], fill="#000000")
