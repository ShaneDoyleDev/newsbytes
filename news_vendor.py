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

    def get_articles(self, category):
        try:
            url = f"{self.BASE_URL}top-headlines?category={self.categories[category]}&language=en&apiKey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()

            # Get articles from response
            articles = response.json().get('articles', [])
            self.selected_articles = []
            while len(self.selected_articles) < 5 and articles:
                article = random.choice(articles)
                # Remove articles with [Removed] in the title
                if '[Removed]' not in article['title']:
                    self.selected_articles.append(article)
                articles.remove(article)

        except requests.ConnectionError:
            # Handle connection errors
            print("Error: Unable to connect to the server.")
        except requests.HTTPError:
            # Handle HTTP errors
            print("Error: An HTTP error occurred.")

    def get_promo_category(self):
        current_day = datetime.datetime.now().weekday()
        if current_day < len(self.categories):
            return self.categories[current_day]
        return None

    def get_promo_message(self, category):
        return self.promo_messages[category]