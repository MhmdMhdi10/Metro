import os
import logging
import re
import pickle

from Exeptions.models import *

from User.models import User
from User.models import PhoneNumber
from User.models import Email
from core.models import DBModel
from core.manager import db


logging.basicConfig(filename='Bank.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')


class CentralBank(DBModel):
    TABLE = "central_bank"
    PK = "id"

    def __init__(self, country):
        self.country = country
        # db.create(self)

    @staticmethod
    def create(country):
        central_bank = CentralBank(country)
        with open(f"central_bank_{country}", "wb") as f:
            pickle.dump(central_bank, f)
        logging.info(f"Central Bank of country: {country} has been created.")
        return central_bank

    @staticmethod
    def get_obj(country):
        with open(f"central_bank_{country}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"Central Bank of country: {country} has been loaded.")
        return obj

# ===================================================================================================================
# ===================================================================================================================
# ===================================================================================================================

class AccountType(DBModel):
    TABLE = "account_type"
    PK = "id"

    def __init__(self, central_bank: CentralBank, account_type: str, minimum_balance, number_of_users: int = 1):
        self.central_bank_id = central_bank
        self.account_type = account_type
        self.minimum_balance = minimum_balance
        self.number_of_users = number_of_users
        # db.create(self)

    @staticmethod
    def create(central_bank: CentralBank, account_type: str, minimum_balance, number_of_users: int = 1):
        account_type = AccountType(central_bank, account_type, minimum_balance, number_of_users)
        with open(f"account_type_{account_type.account_type}", "wb") as f:
            pickle.dump(account_type, f)
        logging.info(f"account type: {account_type.account_type} has been created.")
        return account_type

    @staticmethod
    def get_obj(account_type):
        with open(f"account_type_{account_type}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"account type: {account_type} has been loaded.")
        return obj

    @property
    def central_bank_id(self):
        return self._central_bank_id

    @central_bank_id.setter
    def central_bank_id(self, value):
        if isinstance(value, CentralBank):
            self._central_bank_id = value
        else:
            logging.error(f"Invalid central bank value: {value}")
            raise ValueError("value should be a central_bank obj")

    @property
    def number_of_users(self):
        return self._number_of_users

    @number_of_users.setter
    def number_of_users(self, value):
        if value >= 1 and isinstance(value, int):
            self._number_of_users = value
        else:
            logging.error(f"Invalid number_of_users value: {value}")
            raise ValueError("number of users is not a valid number")

    @property
    def minimum_balance(self):
        return self._minimum_balance

    @minimum_balance.setter
    def minimum_balance(self, value):
        if value >= 0:
            self._minimum_balance = value
        else:
            logging.error(f"Invalid minimum_balance value: {value}")
            raise ValueError("minimum balance should be a positive float or int")

# ===================================================================================================================
# ===================================================================================================================
# ===================================================================================================================

class Bank(DBModel):
    TABLE = "bank"
    PK = "id"
    bank_numbers = []

    def __init__(self, bank_name, central_bank: CentralBank, bank_number):
        self.bank_name = bank_name
        self.central_bank_id = central_bank
        self.bank_number = bank_number
        # db.create(self)

    @staticmethod
    def create(bank_name, central_bank: CentralBank, bank_number):
        bank = Bank(bank_name, central_bank, bank_number)
        with open(f"bank_{bank_number}", "wb") as f:
            pickle.dump(bank, f)
        logging.info(f"bank: {bank_name} with bank_number: {bank.bank_number} has been created.")
        return bank

    @staticmethod
    def get_obj(bank_number):
        with open(f"bank_{bank_number}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"bank: {obj.bank_name} with bank_number: {bank_number} has been edited.")
        return obj

    @property
    def central_bank_id(self):
        return self._central_bank_id

    @central_bank_id.setter
    def central_bank_id(self, value):
        if isinstance(value, CentralBank):
            self._central_bank_id = value
        else:
            logging.error(f"Invalid central_bank: {value}")
            raise ValueError("central bank should be an instance of class 'CentralBank'")

    @property
    def bank_number(self):
        return self._bank_number

    @bank_number.setter
    def bank_number(self, value: str):
        if len(value) == 4 and value.isnumeric() and value not in self.__class__.bank_numbers:
            self._bank_number = value
            self.__class__.bank_numbers.append(value)
        else:
            logging.error(f"Invalid bank_number: {value}")
            raise ValueError("bank number should be 4 digits and unique ")

# ===================================================================================================================
# ===================================================================================================================
# ==================================================================================================================

class BankAccount(DBModel):
    TABLE = "bank_account"
    PK = "id"
    bank_account_numbers = []

    def __init__(self, bank: Bank, user: User, account_type: AccountType, bank_account_number, bank_account_password,
                 email: Email, phone_number: PhoneNumber, balance: int):
        self.user_id = user
        self.bank_id = bank
        self.account_type_id = account_type
        self.bank_account_number = f"{self.bank_id.bank_number}{bank_account_number}"
        self.bank_account_password = bank_account_password
        self.email_id = email
        self.phone_number_id = phone_number
        self.balance = balance
        # db.create(self)

    @staticmethod
    def create(bank: Bank, user: User, account_type: AccountType, bank_account_number, bank_account_password,
               email: Email, phone_number: PhoneNumber, balance: int):
        bank_account = BankAccount(bank, user, account_type, bank_account_number, bank_account_password,
                                   email, phone_number, balance)
        with open(f"bank_account_{bank_account_number}", "wb") as f:
            pickle.dump(bank_account, f)
        bank_account.__class__.bank_account_numbers.append(bank_account.bank_account_number)
        logging.info(f"bank account with bank account_number {bank_account_number} has been created.")
        return bank_account

    @staticmethod
    def get_obj(bank_account_number):
        with open(f"bank_account_{bank_account_number}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"bank account with bank account_number {bank_account_number} has been loaded.")
        return obj

    def edit_password(self, current_pass, new_pass, new_pass_repeat):
        if current_pass == self.bank_account_password:
            if new_pass_repeat == new_pass:
                self.bank_account_password = new_pass
                os.remove(f"bank_account_{self.bank_account_number}")
                with open(f"bank_account_{self.bank_account_number}", "wb") as f:
                    pickle.dump(self, f)
                logging.info(f"password of bank_account: {self.bank_account_number} has been edited")
            else:
                logging.error(f"PassRepeatError: bank_account_number: {self.bank_account_number} on edit password")
                raise PassRepeatError("new passwords dont match")
        else:
            logging.error(f"WrongPassError: Bank_account_number: {self.bank_account_number} on edit password")
            raise WrongPass("current pass is wrong")

    def edit_email(self, new_email):
        self.email_id = Email.get_obj(new_email).email
        with open(f"bank_account_{self.bank_account_number}", "wb") as f:
            pickle.dump(self, f)
        logging.info(f"email on bank_account: {self.bank_account_number} has been edited")

    def edit_phone_number(self, new_phone_number):
        self.phone_number_id = Email.get_obj(new_phone_number).phone_number
        with open(f"bank_account_{self.bank_account_number}", "wb") as f:
            pickle.dump(self, f)
        logging.info(f"phone_number on bank_account: {self.bank_account_number} has been edited")

    @staticmethod
    def delete_account(bank_account_number):
        os.remove(f"metro_account_{bank_account_number}")
        logging.info(f"metro_account: {bank_account_number} has been removed")

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value: User):
        if isinstance(value, User):
            self._user_id = value
        else:
            logging.error(f"WrongPassError: Bank_account_number: {self.bank_account_number} on edit password")
            raise ValueError("user should be an instance class 'User'")

    @property
    def bank_id(self):
        return self._bank_id

    @bank_id.setter
    def bank_id(self, value):
        if isinstance(value, Bank):
            self._bank_id = value
        else:
            logging.error(f"Invalid bank: {value}")
            raise ValueError("bank should be an instance class 'Bank'")

    @property
    def account_type_id(self):
        return self._account_type_id

    @account_type_id.setter
    def account_type_id(self, value):
        if isinstance(value, AccountType):
            self._account_type_id = value
        else:
            logging.error(f"Invalid account_type: {value}")
            raise ValueError("account type should be an instance class 'AccountType'")

    @property
    def bank_account_number(self):
        return self._bank_account_number

    @bank_account_number.setter
    def bank_account_number(self, value):
        if len(value) == 8 and value.isnumeric():
            if value not in self.__class__.bank_account_numbers:
                self._bank_account_number = value
                self.__class__.bank_account_numbers.append(value)
            else:
                logging.error(f"ExistingObjError on bank_account:{self.bank_account_number} with value of: {value}")
                raise ExistingObjError("bank_account number should be unique")
        else:
            logging.error(f"Invalid bank_account_number: {value}")
            raise ValueError("bank account number should be 8 digits ")

    @property
    def bank_account_password(self):
        return self._bank_account_password

    @bank_account_password.setter
    def bank_account_password(self, value):
        # pattern = "^[a-zA-Z\d]{8}$"
        # if not re.search(pattern, str(value)):
        if not 4 <= len(str(value)) <= 8:
            logging.error(f"WeakPassError on bank_account: {self.bank_account_number}")
            raise WeakPass("password should be between 8 and 4 chars with only digits")
        self._bank_account_password = value

    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, value):
        if isinstance(value, Email):
            self._email_id = value
        else:
            logging.error(f"Invalid email: {value}")
            raise ValueError("email should be an instance class 'Email'")

    @property
    def phone_number_id(self):
        return self._phone_number_id

    @phone_number_id.setter
    def phone_number_id(self, value):
        if isinstance(value, PhoneNumber):
            self._phone_number_id = value
        else:
            logging.error(f"Invalid phone_number: {value}")
            raise ValueError("phone number should be an instance class 'PhoneNumber'")

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value > self.account_type_id.minimum_balance:
            self._balance = value
        else:
            logging.error(f"Invalid bank: {value}")
            raise LowMargin("low margin")

    def cash(self, amount):
        if self.balance - self.account_type_id.minimum_balance >= amount:
            self.balance -= amount
            with open(f"bank_account_{self.bank_account_number}", "wb") as f:
                pickle.dump(self, f)
            logging.info(f"bank_account: {self.bank_account_number} has cashed {amount}$")
        else:
            logging.error(f"LowMarginError on bank_account: {self.bank_account_number}")
            raise LowMargin("LowMargin")

    def deposit(self, amount):
        if amount < 0:
            logging.error("a negetive amount was deposited")
            raise ValueError("deposit amount shouldnt be negetive")
        self.balance += amount
        with open(f"bank_account_{self.bank_account_number}", "wb") as f:
            pickle.dump(self, f)
        logging.info(f"bank_account: {self.bank_account_number} has cashed {amount}$")

    def transfer(self, account, amount):
        if self.balance - self.account_type_id.minimum_balance >= amount:
            self.balance -= amount
            with open(f"bank_account_{self.bank_account_number}", "wb") as f:
                pickle.dump(self, f)
            account.balance += amount
            with open(f"bank_account_{account.bank_account_number}", "wb") as f:
                pickle.dump(account, f)
            logging.info(f"bank_account: {self.bank_account_number} has transferred {amount}$ "
                         f"to bank_account {account}")
        else:
            logging.error(f"lowMarginError on bank account: {self.bank_account_number}")
            raise LowMargin("low Margin")

    def show_info(self):
        return f"""name : {self.user_id.first_name} {self.user_id.last_name}
account_number : {self.bank_account_number}
phone_number : {self.phone_number_id.phone_number}
email : {self.email_id.email}
bank : {self.bank_id.bank_name}
account_type : {self.account_type_id.account_type}
balance : {self.balance}
"""


