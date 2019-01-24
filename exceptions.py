class AssetException(Exception):
    pass


class AllocsException(AssetException):
    pass


class InvestmentException(AssetException):
    pass


class BuyDateException(AssetException):
    pass


class BuyPriceException(AssetException):
    pass
