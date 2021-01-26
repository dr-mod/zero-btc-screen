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
        max_price = max(prices)
        min_price = min(prices)
        middle_price = (max_price - min_price) / 2 + min_price
        draw.text(position_first, "%d" % max_price, font=font)
        draw.text((position_first[0], (position_last[1] - position_first[1]) / 2 + position_first[1]), "%d" % middle_price, font=font)
        draw.text(position_last, "%d" % min_price, font=font)

    @staticmethod
    def caption(price, y, screen_width, font, draw):
        price_text = "BTC = %.2f" % price
        text_width, _ = draw.textsize(price_text, font)
        price_position = ((screen_width - text_width) / 2, y)
        draw.text(price_position, price_text, font=font)

