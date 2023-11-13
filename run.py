import os
import pyfiglet
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.table import Table
from user_account import UserAccount
from currency import Currency
from news_vendor import NewsVendor

# Load environment variables from '.env' file.
load_dotenv()
api_key = os.environ.get('API_KEY')

exchange_rate_api_key = os.environ.get('EXCHANGE_RATE_API_KEY')
news_api_key = os.environ.get('NEWS_API_KEY')

console = Console()


def clear_screen():
    """Clears the terminal screen"""
    if os.name == 'nt':  # If the operating system is Windows
        os.system('cls')
    else:
        os.system('printf "\033c"')  # If the operating system is not Windows


def prompt_main_menu():
    """Prompt user to return to main menu"""
    input("\nPress Enter to return to the main menu...")


def main_menu(user, currency, news_vendor):
    """Show Main menu"""
    while True:
        clear_screen()
        console.print("============== NewsBytes ==============",
                      justify="center", style="bold cyan")
        console.print(f"🌐 Welcome to NewsBytes, {user.username}! 🌐",
                      justify="center")
        print("")

        # Create a table instance
        table = Table(show_header=True, header_style="bold cyan",
                      box=box.ROUNDED, show_lines=True, title="Main Menu",
                      title_style="bold cyan")

        # Add columns to the table
        table.add_column("Option", style="cyan", justify="center",
                         no_wrap=True)
        table.add_column("Description", justify="left", style="white")

        # Add rows to the table with the menu options
        table.add_row("(1)", f"Add Funds ({currency.symbol}{user.funds:.2f})")
        table.add_row("(2)",
                      "Purchase Credits ({} credits)".format(user.credits))
        table.add_row("(3)", "Purchase News Article")
        table.add_row("(4)", f"View Your Articles "
                      f"({len(user.purchased_articles)} articles)")
        table.add_row("(5)", "Exit")

        # Print the table to the console
        console.print(table, justify="center")
        print("")

        # Get user's choice
        choice = input("Select your choice (1 - 5): ")

        # Process user's choice
        if choice == "1":
            add_funds(user, currency)
        elif choice == "2":
            purchase_credits(user, currency, news_vendor)
        elif choice == "3":
            purchase_article(user, news_vendor)
        elif choice == "4":
            view_purchased_articles(user)
        elif choice == "5":
            exit_program()
        else:
            console.print("❌ Invalid choice. Please select a number"
                          "between 1 and 5.", style="bold red")


def add_funds(user, currency):
    """Add funds to user's account"""
    clear_screen()
    console.print("============ Add Funds ============",
                  justify="center", style="bold cyan")
    console.print(f"💰 Account Funds: ({currency.symbol}{user.funds:.2f})",
                  justify="center")
    print("")

    while True:
        amount = input(
            f"Enter amount to add in {currency.currency_code}: ").strip()
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
                console.print(f"✅ {currency.symbol}{amount_float:.2f} added "
                              "successfully!", style="bold green")
                prompt_main_menu()
                break
        except ValueError:
            print("❌ Amount must be a number. Please try again!")


def purchase_credits(user, currency, news_vendor):
    """Purchase credits for users account"""
    clear_screen()
    console.print("========= Purchase Credits =========",
                  justify="center", style="bold cyan")
    console.print(f"💳 Account Credits: ({user.credits})",
                  justify="center")
    print("")

    # Create a table for purchasing credits
    credits_table = Table(
        show_header=True, header_style="bold magenta", box=box.ROUNDED,
        show_lines=True, title="Credit Packages", title_style="bold cyan")

    # Add columns to the table
    credits_table.add_column("Option", style="cyan", justify="center",
                             no_wrap=True)
    credits_table.add_column("Credits", justify="center", style="white")
    credits_table.add_column("Cost", justify="center", style="green")

    # Add rows to the table with the credit purchase options
    for idx, option in enumerate(news_vendor.credit_options, 1):
        credits_table.add_row(f"({idx})", f"{option} credits",
                              f"{currency.symbol}"
                              f"{option * currency.conversion_rate:.2f}")

    # Print the table to the console
    console.print(credits_table, justify="center")
    print("")

    while True:
        credits_choice = input(
            f"Select credit package to purchase "
            f"(1 - {len(news_vendor.credit_options)}), "
            "or enter 'back' to go back: ").strip().lower()

        # Check if user wants to go back to main menu
        if credits_choice == 'back':
            break

        # Check if user entered a valid credit selection
        if not (credits_choice.isdigit() and
                1 <= int(credits_choice) <= len(news_vendor.credit_options)):
            console.print(
                          "❌ Invalid choice. Please "
                          "select a valid option "
                          "from the table.", style="bold red")
            continue
        else:
            credits_index = int(credits_choice) - 1
            credits_amount = news_vendor.credit_options[credits_index]
            cost = credits_amount * currency.conversion_rate

            if user.funds >= cost:
                user.purchase_credits(credits_amount, cost)
                console.print(
                    f"✅ {credits_amount} credits purchased successfully for "
                    f"{currency.symbol}{cost:.2f}!", style="bold green")
            else:
                console.print(
                    f"❌ Insufficient funds. "
                    "You need {currency.symbol}{cost - user.funds:.2f} "
                    "more to purchase this package.", style="bold red")

            prompt_main_menu()
            break


def purchase_article(user, news_vendor):
    """Purchase news articles"""
    clear_screen()
    console.print("====== Purchase News Article ======",
                  justify="center", style="bold cyan")
    console.print(f"💳 Account Credits: ({user.credits})",
                  justify="center")
    print("")

    promo_category = news_vendor.get_promo_category()

    table = Table(show_header=True, header_style="bold cyan",
                  box=box.ROUNDED, show_lines=True,
                  title="News Categories", title_style="bold cyan")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Category", justify="center", style="white")
    table.add_column("Cost", justify="center", style="green")

    # show categories
    for idx, category in enumerate(news_vendor.categories, 1):
        # add promo message to category if it is the promo category
        if category == promo_category:
            table.add_row(f"({idx})",
                          f"{category.title()}"
                          f"- {news_vendor.get_promo_message(category)}",
                          "1 credit")
        else:
            table.add_row(f"({idx})", f"{category.title()}", "2 credits")

    console.print(table)

    while True:
        # get category choice
        print("")
        category_choice = input(
            f"Select category (1 - {len(news_vendor.categories)}): ").strip()

        if not category_choice:
            print("❌ Category cannot be empty. Please try again!")
            continue

        valid_options = map(str,
                            range(1, len(news_vendor.categories) + 1))
        if category_choice not in valid_options:
            print("❌ Please enter a valid option!")
            continue

        # get selected category
        selected_category = int(category_choice) - 1
        break

    # choose a news article from category
    clear_screen()
    console.print(
        f"🌍 Todays top international stories in "
        f"{news_vendor.categories[selected_category]} 🌍",
        justify="center", style="cyan")
    print("")

    # get and display articles from news vendor
    news_vendor.get_articles(selected_category)
    print("")

    # Display articles in a table
    articles_table = Table(
        show_header=True, header_style="bold cyan", box=box.ROUNDED,
        show_lines=True, title="Available Articles", title_style="bold cyan")

    # Add columns to the articles table
    articles_table.add_column("No.", style="cyan", justify="center")
    articles_table.add_column("Title", style="white", justify="left")
    articles_table.add_column("Author", style="green", justify="left")
    articles_table.add_column("Published At", style="magenta", justify="left")

    # Add rows to the articles table
    for idx, article in enumerate(news_vendor.selected_articles, 1):
        articles_table.add_row(
            f"({idx})", article['title'],
            article['author'] if 'author' in article else "N/A",
            article['publishedAt'])

    # Print the articles table
    console.print(articles_table)
    print(f"💳 Account Credits: ({user.credits})")

    while True:
        # get article choice
        selected_articles_length = len(news_vendor.selected_articles)
        article_choice = input(
            f"Select article (1 - "
            f"{selected_articles_length}): ").strip()

        # check for valid choice
        article_range = range(1, selected_articles_length + 1)
        if article_choice not in map(str, article_range) or \
           not article_choice:
            print("❌ Please enter a valid option!")
            continue

        # get selected article
        article_index = int(article_choice) - 1
        selected_article = news_vendor.selected_articles[article_index]

        # check if article discount applies
        if news_vendor.categories[selected_category] == promo_category:
            article_price = 1
        else:
            article_price = 2

        # check if user has enough credits
        if user.credits < article_price:
            clear_screen()
            console.print(f"❌ You don't have enough credits. ❌",
                          style="bold red", justify="center")
            console.print(f"These articles cost {article_price} credits each. "
                          "Please top up your account!", justify="center")
            prompt_main_menu()
            break

        # purchase article and deduct account credits
        user.credits -= article_price
        user.purchased_articles.append(selected_article)
        print(f"🎉 Article purchased for {article_price} credits!")
        break


def view_purchased_articles(user):
    """View purchased articles"""
    clear_screen()
    console.print("======== Your Articles =========",
                  justify="center", style="bold cyan")

    if not user.purchased_articles:
        console.print("You have not purchased any articles yet!",
                      style="bold red")
    else:
        # Loop through each purchased article
        for idx, article in enumerate(user.purchased_articles, 1):
            # Create a table for this particular article
            article_table = Table(
                show_header=True, header_style="bold cyan",
                box=box.ROUNDED, show_lines=True)

            # Add columns to the article table
            article_table.add_column("No.", style="cyan",
                                     justify="center", no_wrap=True)
            article_table.add_column("Title", justify="center", style="white")
            article_table.add_column("Description", justify="center",
                                     style="white")

            # Add the article details as a row
            article_table.add_row(
                str(idx),
                article['title'],
                article['description'] or
                "No description available."
            )

            console.print(article_table, justify="center")

            # Display the article's access link below each table
            console.print(f"\n🔗 [bold blue]Access Link:[/] {article['url']}\n",
                          justify="center")

    print("")
    prompt_main_menu()


def exit_program():
    """Exit program and display goodbye message"""
    clear_screen()
    print(pyfiglet.figlet_format("Goodbye!", font="slant", justify="center"))
    console.print("👋 Thank you for using NewsBytes!",
                  justify="center")
    console.print("Have a great day!",
                  justify="center")
    exit()


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
        currency = input("💰 Select your currency "
                         "(EUR, USD, GBP, CAD, AUD, CNY): \n")\
            .strip().upper()
        if currency not in valid_currencies or not currency:
            print("❌ Please enter a valid currency!")
        else:
            break

    # instantiate user class
    user = UserAccount(username)

    # instantiate currency class
    currency = Currency(exchange_rate_api_key, currency)

    # instantiate news vendor class
    news_vendor = NewsVendor(news_api_key)

    # show main menu
    main_menu(user, currency, news_vendor)


if __name__ == "__main__":
    main()
