import pickle
import logging

from Exeptions.models import *
from core.models import DBModel
from core.manager import db
import re

logging.basicConfig(filename='User.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')


class User(DBModel):
    TABLE = "user"
    PK = "id"

    def __init__(self, first_name: str, last_name: str, national_id: str):
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        # db.create(self)

    @staticmethod
    def create(first_name: str, last_name: str, national_id: str):
        user = User(first_name, last_name, national_id)
        with open(f"User_{national_id}", "wb") as f:
            pickle.dump(user, f)
        logging.info(f'User with national ID: {national_id} has been created.')
        return user

    @staticmethod
    def get_obj(national_id):
        with open(f"User_{national_id}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f'User with national ID: {national_id} has been loaded.')
        return obj

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha():
            self._first_name = value
        else:
            logging.error(f'Invalid first name: {value}')
            raise ValueError("first name should only have alphabets")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha():
            self._last_name = value
        else:
            logging.error(f'Invalid last name: {value}')
            raise ValueError("last name should only have alphabets")

    @property
    def national_id(self):
        return self._national_id

    @national_id.setter
    def national_id(self, value: str):
        if len(value) == 10 and value.isnumeric():
            self._national_id = value
        else:
            logging.error(f'Invalid national ID: {value}')
            raise ValueError("national id is not valid")


# ===================================================================================================================
# ===================================================================================================================
# ===================================================================================================================
class PhoneNumber(DBModel):
    TABLE = "phone_number"
    PK = "id"
    phone_numbers = []

    def __init__(self, user: User, phone_number, company):
        self.user_id = user
        self.phone_number = phone_number
        self.company = company
        # db.create(self)

    @staticmethod
    def create(user: User, phone_number, company):
        phone_number = PhoneNumber(user, phone_number, company)
        with open(f"User_{phone_number.phone_number}", "wb") as f:
            pickle.dump(phone_number, f)
        phone_number.__class__.phone_numbers.append(phone_number.phone_number)
        logging.info(f'Phone_number with Phone_number: {phone_number.phone_number} has been created.')
        return phone_number

    @staticmethod
    def get_obj(phone_number):
        with open(f"User_{phone_number}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f'Phone_number with Phone_number: {phone_number.phone_number} has been loaded.')
        return obj

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, User):
            self._user_id = value
        else:
            logging.error(f'Invalid user used in PhoneNumber: {value}')
            raise ValueError("user should be from class 'User'")

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        pattern = "^09\d{9}$"
        if not re.search(pattern, str(value)):
            logging.error(f'Invalid phone_number: {value}')
            raise ValueError("Invalid phone number")
        elif value in self.__class__.phone_numbers:
            logging.error(f'used repetitive phone_number: {value}')
            raise ExistingObjError("phone number exists")
        else:
            self._phone_number = value


# ===================================================================================================================
# ===================================================================================================================
# ===================================================================================================================
class Email(DBModel):
    TABLE = "email"
    PK = "id"

    def __init__(self, user: User, email):
        self.user_id = user
        self.email = email
        # db.create(self)

    @staticmethod
    def create(user: User, email):
        email_obj = Email(user, email)
        with open(f"User_{email}", "wb") as f:
            pickle.dump(email_obj, f)
        logging.info(f'Email with email_address: {email} has been created.')
        return email_obj

    @staticmethod
    def get_obj(email):
        with open(f"User_{email}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f'Email with email_address: {email} has been loaded.')
        return obj

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, User):
            self._user_id = value
        else:
            logging.error(f'Invalid user used in Email: {value}')
            raise ValueError("user should be from class 'User'")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.search(pattern, str(value)):
            logging.error(f'Invalid Email_address: {value}')
            raise ValueError("Invalid email address")
        self._email = value
