import os
import pyfiglet
from dotenv import load_dotenv


def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

