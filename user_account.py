class UserAccount:
    """User with username and credits."""
    def __init__(self, username):
        self.username = username.title()
        self.funds = 0.0
        self.credits = 0
        self.purchased_articles = []

    def add_funds(self, amount):
        """Add funds to user's account."""
        self.funds += round(amount, 2)

    def purchase_credits(self, credits_amount, cost):
        """Purchase credits for user's account."""
        if self.funds >= cost:
            self.credits += credits_amount
            self.funds -= cost
