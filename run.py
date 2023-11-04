import os
import pyfiglet
from dotenv import load_dotenv
from user_account import UserAccount
from currency import Currency
from news_vendor import NewsVendor

# Load environment variables from '.env' file.
load_dotenv()
api_key = os.environ.get('API_KEY')

exchange_rate_api_key = os.environ.get('EXCHANGE_RATE_API_KEY')
news_api_key = os.environ.get('NEWS_API_KEY')

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main function."""
    clear_screen()

    LOGO = pyfiglet.figlet_format("NewsBytes", justify="center", font="slant")
    print(LOGO)

    # get username
    while True:
        username = input("👤 Enter your username: \n").strip()
        if not username:
            print("❌ Username cannot be empty. Please try again!")
        elif not all(name.isalpha() for name in username.split()):
            print("❌ Username should only contain letters. Please try again!")
        else:
            break

    # get user's currency
    while True:
        valid_currencies = ("USD", "EUR", "GBP", "CAD", "AUD", "CNY")
        currency = input("💰 Select your currency (EUR, USD, GBP, CAD, AUD, CNY): \n").strip().upper()
        if not currency in valid_currencies or not currency:
            print("❌ Please enter a valid currency!")
        else:
            break

    # instantiate user class
    user = UserAccount(username)

    # instantiate currency class
    currency = Currency(exchange_rate_api_key, currency)

    # instantiate news vendor class
    news_vendor = NewsVendor(news_api_key)

    while True:
        clear_screen()
        print("============== MENU ==============")
        print(f"👋 Welcome to NewsBytes, {user.username}!")
        print("")

        # Main menu options
        choice = input(f"Please select an option:\n(1) Add Funds (💰 {currency.symbol}{user.funds:.2f})\n(2) Purchase Credits (💳 {user.credits} credits)\n(3) Purchase News Article\n(4) View Your Articles (📰 {len(user.purchased_articles)} articles)\n(5) Exit\nYour choice: ")

        # Add funds to user's account
        if choice == "1":
            clear_screen()
            print("============ Add Funds ============")
            print(f"💰 Account Funds: ({currency.symbol}{user.funds:.2f})")
            print("")

            while True:
                amount = input(f"Enter amount to add in {currency.currency_code}: ").strip()
                # Check for empty input
                if not amount:
                    print("❌ Amount cannot be empty. Please try again!")
                    continue
                try:
                    # Convert input to float and check its value
                    amount_float = float(amount)
                    if amount_float <= 0:
                        print("❌ Amount must be greater than 0. Please try again!")
                        continue
                    else:
                        # Add funds to user's account
                        user.add_funds(amount_float)
                        break
                except ValueError:
                    print("❌ Amount must be a number. Please try again!")


if __name__ == "__main__":
    main()