import requests

class Currency:
    """
    Currency class for working with currency exchange rates and symbols.

    This class allows you to fetch exchange rates for a specified currency
    and retrieve the currency symbol based on the currency code.
    """

    BASE_URL = "https://v6.exchangerate-api.com/v6/"
    CURRENCY_SYMBOLS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "CAD": "$",
        "AUD": "$",
        "CNY": "¥"
    }

    def __init__(self, api_key, currency_code):
        self.api_key = api_key
        self.currency_code = currency_code
        self.symbol = self.get_symbol(currency_code)
        self.conversion_rate = self._fetch_exchange_rate(currency_code)
