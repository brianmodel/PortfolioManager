from datetime import datetime
import json

from exceptions import AssetException


class Assets:
    # {
    #     "APPL": {
    #         "shares": 5,
    #         "buy_date": datetime(),
    #         "buy_price": optional parameter of price at which asset was bought
    #     }
    # }
    # {
    #     "investment": 100
    #     "APPL": {
    #         "alloc": .5,
    #         "buy_date": datetime(),
    #         "buy_price": optional
    #     }
    # }
    # ["APPl", "GOOG"], 100, [.5, .5], [buy_date, buy_date]
    def __init__(self, investment, tickers, allocs, buy_dates, buy_price=None):
        self.investment = investment
        self.tickers = tickers
        self.allocs = allocs
        self.buy_dates = buy_dates
        self.json_assets = self.as_json()
        if buy_price != None:
            self.buy_price = buy_price

    @classmethod
    def from_json(cls, assets):
        investment = 0
        tickers = []
        allocs = []
        buy_dates = []

        for ticker in assets:
            tickers.append(ticker)
            num_shares = assets[ticker]["shares"]
            try:
                datetime.strptime(assets[ticker]["buy_date"], "%Y-%m-%d")
                buy_dates = assets[ticker]["buy_date"]
            except (ValueError, TypeError) as e:
                raise AssetException(
                    '"buy_date" parameter must be a date in the format of YYYY-MM-DD.'
                )
            buy_price = None
            if "buy_price" in assets[ticker]:
                try:
                    buy_price = float(assets[ticker]["buy_price"])
                except ValueError:
                    raise AssetException(
                        'Optional "buy_price" parameter must be a number.'
                    )



        return cls(investment, tickers, allocs, buy_dates)

    def as_json(self):
        assets = {}
        for ticker, alloc in zip(self.tickers, self.allocs):
            assets[ticker] = {}
            assets[ticker]["alloc"] = alloc
            assets[ticker]["buy"] = self.investment * alloc
        print(assets)
        return assets

    def __str__(self):
        pass


if __name__ == "__main__":
    assets_json = {"APPL": {"shares": 5, "buy_date": 100}}
    assets = Assets.from_json(assets_json)
    print("Investment ", assets.investment)
    print("Tickers ", assets.tickers)
    print("Allocs ", assets.allocs)
    print("Buy dates ", assets.buy_dates)

    assets.as_json()
