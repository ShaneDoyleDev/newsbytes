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

    def get_symbol(self, currency_code):
        """Retrieve the currency symbol based on the currency code."""
        return self.CURRENCY_SYMBOLS.get(currency_code, "")

    def _fetch_exchange_rate(self, currency_code):
        """
        Private method to fetch the exchange rate
        for a specified amount between USD and selected currency type.
        """
        url = f"{self.BASE_URL}{self.api_key}/pair/USD/{currency_code}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            if data['result'] == 'error':
                raise Exception(data['error-type'])

            return data['conversion_rate']

        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            raise Exception("A network problem occurred. "
                            "Please check your connection.")

        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while "
                            "fetching the exchange rate. Error: {e}")
