from colorama import Fore
from colorama import Style

class Error:
    def __init__(self, message):
        self.message = message

    def show(self):
        print(f"{Fore.RED}ERROR! {self.message}{Style.RESET_ALL}")