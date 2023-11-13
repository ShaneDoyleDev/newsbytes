import os
import pyfiglet
from dotenv import load_dotenv

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

if __name__ == "__main__":
    main()