from datetime import datetime
import json

from exceptions import *


class Assets:
    # {
    #     "investment": 100,
    #     "portfolio": {
    #         "APPL": {
    #             "alloc": .5,
    #             "buy_date": datetime(),
    #             "buy_price": optional
    #         }
    #     }
    # }
    # ["APPl", "GOOG"], 100, [.5, .5], [buy_date, buy_date]
    def __init__(self, investment, tickers, allocs, buy_dates, buy_prices):
        self.investment = investment
        self.tickers = tickers
        self.allocs = allocs
        self.buy_dates = buy_dates
        self.buy_prices = buy_prices
        self.json_assets = self.as_json()

    @classmethod
    def from_json(cls, assets):
        investment = 0
        tickers = []
        allocs = []
        buy_dates = []
        buy_prices = []

        try:
            investment = float(assets["investment"])
        except Exception:
            raise InvestmentException("Investment parameter must be a float.")

        portfolio = assets["portfolio"]
        for ticker in portfolio:
            tickers.append(ticker)

            try:
                alloc = float(portfolio[ticker]["alloc"])
                # assert alloc > 0 and alloc <= 1
            except Exception:
                raise AllocsException(
                    "Alloc value must be a float between 0 exclusive and 1 inclusive."
                )

            try:
                datetime.strptime(portfolio[ticker]["buy_date"], "%Y-%m-%d")
                buy_date = portfolio[ticker]["buy_date"]
            except (ValueError, TypeError):
                raise BuyDateException(
                    '"buy_date" parameter must be a date in the format of YYYY-MM-DD.'
                )
            buy_price = None
            if "buy_price" in portfolio[ticker]:
                try:
                    buy_price = float(portfolio[ticker]["buy_price"])
                except ValueError:
                    raise BuyPriceException(
                        'Optional "buy_price" parameter must be a number.'
                    )
            allocs.append(alloc)
            buy_dates.append(buy_date)
            buy_prices.append(buy_price)

        return cls(investment, tickers, allocs, buy_dates, buy_prices)

    def as_json(self):
        # investment, tickers, allocs, buy_dates, buy_prices=[]
        assets = {}
        assets["investment"] = self.investment
        assets["portfolio"] = {}
        portfolio = assets["portfolio"]

        for ticker, alloc, buy_date, buy_price in zip(
            self.tickers, self.allocs, self.buy_dates, self.buy_prices
        ):
            portfolio[ticker] = {}
            portfolio[ticker]["alloc"] = alloc
            portfolio[ticker]["buy_date"] = buy_date
            portfolio[ticker]["buy_price"] = buy_price
        return assets

    def __str__(self):
        return json.dumps(self.as_json())


if __name__ == "__main__":
    assets_json = {
        "investment": 100,
        "portfolio": {
            "APPL": {"alloc": 0.5, "buy_date": "2015-04-13", "buy_price": 100},
            "GOOG": {"alloc": 0.5, "buy_date": "2015-04-13"},
        },
    }
    assets = Assets.from_json(assets_json)
    print("Investment ", assets.investment)
    print("Tickers ", assets.tickers)
    print("Allocs ", assets.allocs)
    print("Buy dates ", assets.buy_dates)
    print("Buy prices ", assets.buy_prices)

    print(assets)
