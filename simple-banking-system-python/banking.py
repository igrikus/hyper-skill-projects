import random
import sqlite3


def init_card_db(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
    );
    """)
    connection.commit()
    return cursor


class Bank:
    connection = sqlite3.connect("card.s3db")
    card_db = init_card_db(connection)

    class Card:
        def __init__(self, card_number, card_pin, balance=0):
            self.card_number = card_number
            self.card_pin = card_pin
            self.balance = balance

        def check_balance(self):
            Bank.card_db.execute(f"""
                SELECT balance FROM card
                WHERE number = {self.card_number}
            """)
            balance = Bank.card_db.fetchone()[0]
            return int(balance)

        def update_balance(self, new_balance):
            Bank.card_db.execute(f"""
                UPDATE card
                    SET balance = {new_balance}
                WHERE number = {self.card_number}
            """)
            Bank.connection.commit()
            self.balance = new_balance

        @staticmethod
        def get_account_identifier(card_number):
            return card_number[6:]

    def show_main_menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        self.__ask_input_in_main_menu()

    def __ask_input_in_main_menu(self):
        command = input()
        print()
        if command == "1":
            self.__create_an_account()
        elif command == "2":
            self.__log_into_account()
        elif command == "0":
            self.__exit()
        else:
            self.__ask_input_in_main_menu()

    def __create_an_account(self):
        card_number = self.__create_new_card_number()
        pin = self.__create_new_pin()
        self.__add_card_into_db(card_number, pin)
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(pin)
        print()
        self.show_main_menu()

    def __create_new_card_number(self):
        bank_identifier = "400000"
        account_identifier = self.__create_account_identifier()
        check_sum = self.__get_check_sum(bank_identifier + account_identifier)
        return bank_identifier + account_identifier + check_sum

    def __create_account_identifier(self):
        numbers = []
        for _ in range(9):
            number = random.randint(0, 9)
            numbers.append(str(number))
        account_identifier = "".join(numbers)

        self.card_db.execute("SELECT * FROM card")
        all_cards = self.card_db.fetchall()
        for card in all_cards:
            card_number = card[1]
            if account_identifier == Bank.Card.get_account_identifier(card_number):
                account_identifier = self.__create_account_identifier()
        return account_identifier

    def __log_into_account(self):
        print("Enter your card number:")
        card_number = input()
        print("Enter your PIN:")
        pin = input()
        card = self.__check_creds(card_number, pin)
        print()
        if card != 0:
            print("You have successfully logged in!")
            print()
            self.__show_card_menu(card)
        else:
            print("Wrong card number or PIN!")
            print()
            self.show_main_menu()

    def __show_card_menu(self, card):
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        self.__ask_input_in_card_menu(card)

    def __ask_input_in_card_menu(self, card):
        command = input()
        print()
        if command == "1":
            self.__show_balance(card)
            self.__show_card_menu(card)
        elif command == "2":
            self.__add_income(card)
            self.__show_card_menu(card)
        elif command == "3":
            self.__do_transfer(card)
            self.__show_card_menu(card)
        elif command == "4":
            self.__close_account(card)
            self.show_main_menu()
        elif command == "5":
            self.__log_out()
        elif command == "0":
            self.__exit()
        else:
            self.__ask_input_in_card_menu(card)

    def __do_transfer(self, card):
        print("\nTransfer")
        card_number = input("Enter card number:\n")
        if not self.__is_card_number_correct(card_number):
            print("Probably you made a mistake in the card number. Please try again!\n")
            self.__show_card_menu(card)
            return
        Bank.card_db.execute(f"""
            SELECT * FROM card
            WHERE number = {card_number}
        """)
        query_result = Bank.card_db.fetchone()
        if not query_result:
            print("Such a card does not exist.\n")
            self.__show_card_menu(card)
            return
        transfer_card = Bank.Card(query_result[1], query_result[2], query_result[3])
        input_balance = int(input("Enter how much money you want to transfer:\n"))
        if input_balance > card.balance or input_balance < 0:
            print("Not enough money!\n")
            self.__show_card_menu(card)
            return
        transfer_card.balance += input_balance
        transfer_card.update_balance(transfer_card.balance)
        card.update_balance(card.balance - input_balance)
        print("Success!\n")
        self.__show_card_menu(card)

    def __close_account(self, card):
        Bank.card_db.execute(f"""
            DELETE FROM card
            WHERE number = {card.card_number}
        """)
        Bank.connection.commit()
        print("The account has been closed!\n")
        self.show_main_menu()

    def __log_out(self):
        print("You have successfully logged out!")
        print()
        self.show_main_menu()

    def __add_card_into_db(self, card_number, pin):
        self.card_db.execute(f"""
        INSERT INTO card (number, pin) VALUES
        (
            {card_number},
            {pin}
        )
        """)
        self.connection.commit()

    def __check_creds(self, card_number, pin):
        self.card_db.execute("SELECT * FROM card")
        all_cards = self.card_db.fetchall()
        for card in all_cards:
            checking_number = card[1]
            checking_pin = card[2]
            balance = card[3]
            if checking_number == card_number and checking_pin == pin:
                return Bank.Card(card_number, pin, balance)
        return 0

    @staticmethod
    def __add_income(card):
        balance = int(input("Enter income:\n"))
        balance += card.check_balance()
        card.update_balance(balance)
        print("Income was added!\n")

    def __is_card_number_correct(self, card_number):
        if len(card_number) != 16:
            return False
        our_last_digit = card_number[-1]
        correct_last_digit = self.__get_check_sum(card_number[:-1])
        return True if our_last_digit == correct_last_digit else False

    @staticmethod
    def __get_check_sum(card_without_last_digit):
        luhn_numbers = []
        need_to_multiply = True
        for number in card_without_last_digit:
            number = int(number)
            if need_to_multiply:
                number *= 2
                need_to_multiply = False
            else:
                need_to_multiply = True
            if number > 9:
                number -= 9
            luhn_numbers.append(number)
        luhn_sum = sum(luhn_numbers)
        check_sum = 10 - abs(luhn_sum % 10)
        return str(check_sum)[-1]

    @staticmethod
    def __create_new_pin():
        numbers = []
        for _ in range(4):
            number = random.randint(0, 9)
            numbers.append(str(number))
        return "".join(numbers)

    @staticmethod
    def __show_balance(card):
        print(f"Balance: {card.balance}")
        print()

    @staticmethod
    def __exit():
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    atm = Bank()
    atm.show_main_menu()
