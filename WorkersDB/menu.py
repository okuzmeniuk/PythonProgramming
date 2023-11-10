class Menu:
    END_SYMBOL = '.'
    DEFAULT_END_STATEMENT = "end the program"

    def __init__(self, menu_options, menu_functions=None, end_statement=DEFAULT_END_STATEMENT):
        self.menu_options = menu_options
        self.menu_functions = menu_functions
        self.end_statement = end_statement

    def __str__(self):
        message = ""
        for key, option in self.menu_options.items():
            message += f"Enter '{key}' to {option}\n"

        message += f"Enter {self.END_SYMBOL} to {self.end_statement}."
        return message

    def get_choice(self):
        choice = None
        while choice not in self.menu_options and choice != self.END_SYMBOL:
            choice = input("Choose one from the above: ").strip()

        return choice

    def run(self, main_object):
        while True:
            print(self)

            choice = self.get_choice()
            if choice == self.END_SYMBOL:
                break

            print('-' * 50)
            self.menu_functions[choice](main_object)
            print('\n' + '=' * 50)