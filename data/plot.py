class Plot:
    @staticmethod
    def line(prices, size=(100, 100), position=(0, 0), draw=None):
        max_price = max(prices)
        min_price = min(prices)
        normalised_prices = [(price - min_price) / (max_price - min_price) for price in prices]
        plot_data = []
        for i, element in enumerate(normalised_prices):
            x = i * (size[0] / len(normalised_prices)) + position[0]
            y = size[1] - (element * size[1]) + position[1]
            plot_data.append((x, y))
        draw.line(plot_data)
