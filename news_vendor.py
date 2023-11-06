import datetime
import random
import requests

class NewsVendor:
    """News vendor for displaying and allowing the purchase of news articles."""

    BASE_URL = "https://newsapi.org/v2/"

    def __init__(self, api_key):
        self.api_key = api_key
        self.credit_options = [5, 10, 15, 20]
        self.selected_articles = []
        self.categories = ["sports", "business", "technology", "entertainment", "politics", "science", "health"]
        self.promo_messages = {
            "sports": "All sports articles are 50% off today!",
            "business": "All business articles are 50% off today!",
            "technology": "All technology articles are 50% off today!",
            "entertainment": "All entertainment articles are 50% off today!",
            "politics": "All politics articles are 50% off today!",
            "science": "All science articles are 50% off today!",
            "health": "All health articles are 50% off today!"
        }
