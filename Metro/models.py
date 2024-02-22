import pickle
import random
import os
import logging

from Exeptions.models import *
from User.models import User
from User.models import PhoneNumber
from User.models import Email
from core.models import DBModel
from core.manager import db

import datetime
import re


logging.basicConfig(filename='Metro.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')


class MetroAccount(DBModel):
    TABLE = "metro_account"
    PK = "id"
    metro_usernames = []

    def __init__(self, user: User, metro_username, metro_password, super_user: bool, banned: bool, email: Email,
                 phone_number: PhoneNumber):
        self.user_id = user
        self.email_id = email
        self.phone_number_id = phone_number
        self.metro_username = metro_username
        self.metro_password = metro_password
        self.super_user = super_user
        self.banned = banned
        # db.create(self)

    @staticmethod
    def create(user: User, metro_username, metro_password, super_user: bool, banned: bool, email: Email,
               phone_number: PhoneNumber):
        metro_account = MetroAccount(user, metro_username, metro_password, super_user, False, email, phone_number)
        with open(f"metro_account_{metro_username}", "wb") as f:
            pickle.dump(metro_account, f)
        logging.info(f"Metro Account with Metro Username: {metro_username} has been created.")
        return metro_account

    @staticmethod
    def get_obj(metro_username):
        with open(f"metro_account_{metro_username}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"Metro Account with Metro Username: {metro_username} has been loaded.")
        return obj

    @staticmethod
    def add_admin(admin, account_username):
        if admin.super_user is True:
            with open(f"metro_account_{account_username}", "rb") as f:
                obj: MetroAccount = pickle.load(f)
            obj.super_user = True
            logging.info(f"metro_account with username: {account_username} has been made "
                         f"an admin by {admin.metro_username}")
            db.update(obj.super_user)

    @staticmethod
    def ban_user(admin, account_username):
        if admin.super_user is True:
            with open(f"metro_account_{account_username}", "rb") as f:
                obj: MetroAccount = pickle.load(f)
            obj.banned = True
            logging.info(f"metro_account with username: {account_username} has been banned by {admin.metro_username}")
            db.update(obj.banned)

    def edit_username(self, new_username):
        if new_username not in self.__class__.metro_usernames:
            self.__class__.metro_usernames.remove(self.metro_username)
            self.metro_username = new_username
            self.__class__.metro_usernames.append(new_username)
            with open(f"metro_account_{self.metro_username}", "wb") as f:
                pickle.dump(self, f)
            db.update(self.metro_username)
            logging.info(f"the username of Metro Account: {self.metro_username} has been edited")
        else:
            logging.error(f'used existing username for a username edit: {new_username}')
            raise ExistingObjError("username already exists")


    def edit_password(self, current_pass, new_pass, new_pass_repeat):
        if current_pass == self.metro_password:
            if new_pass_repeat == new_pass:
                self.metro_password = new_pass
                with open(f"metro_account_{self.metro_username}", "wb") as f:
                    pickle.dump(self, f)
                logging.info(f"the password of Metro Account: {self.metro_username} has been edited")
                db.update(self.metro_password)
            else:
                logging.error(f'new passwords doesnt match (edit password)')
                raise PassRepeatError("new passwords doesnt match")
        else:
            logging.error(f'wrong pass (edit password')
            raise WrongPass("current pass is wrong")

    def edit_email(self, new_email):
        self.email_id = Email.get_obj(new_email).email
        with open(f"metro_account_{self.metro_username}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.email_id)
        logging.info(f"the email of Metro Account: {self.metro_username} has been edited")

    def edit_phone_number(self, new_phone_number):
        self.phone_number_id = Email.get_obj(new_phone_number).phone_number
        with open(f"metro_account_{self.metro_username}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.phone_number_id)
        logging.info(f"the phone_number of Metro Account: {self.metro_username} has been edited")

    @staticmethod
    def delete_account(metro_username):
        os.remove(f"metro_account_{metro_username}")
        obj = MetroAccount.get_obj(metro_username)
        db.delete(obj)
        logging.info(f"Metro Account: {metro_username} has been removed")

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, User):
            self._user_id = value
        else:
            logging.error(f"Invalid user: {value}")
            raise ValueError("user should be an instance of class 'User'")

    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, value):
        if isinstance(value, Email):
            self._email_id = value
        else:
            logging.error(f"Invalid email: {value}")
            raise ValueError("email should be an instance of class 'Email'")

    @property
    def phone_number_id(self):
        return self._phone_number_id

    @phone_number_id.setter
    def phone_number_id(self, value):
        if isinstance(value, PhoneNumber):
            self._phone_number_id = value
        else:
            logging.error(f"Invalid phone_number: {value}")
            raise ValueError("phone number should be an instance of class 'PhoneNumber'")

    @property
    def metro_username(self):
        return self._metro_username

    @metro_username.setter
    def metro_username(self, value):
        if value not in self.__class__.metro_usernames:
            self._metro_username = value
            self.__class__.metro_usernames.append(value)
        else:
            logging.error(f"used existing username: {value}")
            raise ExistingObjError("username already exists")

    @property
    def metro_password(self):
        return self._metro_password

    @metro_password.setter
    def metro_password(self, value):
        pattern = "^\d{4,8}$"
        if not re.search(pattern, str(value)):
            logging.error(f"Weak password: {value}")
            raise WeakPass("password should be between 8 and 4 chars with only digits")
        self._metro_password = value

    @property
    def banned(self):
        return self._banned

    @banned.setter
    def banned(self, value):
        if isinstance(value, bool):
            self._banned = value
        else:
            logging.error(f"Invalid value used as banned: {value}")
            raise ValueError("banned instance should be a boolean")

    @property
    def super_user(self):
        return self._super_user

    @super_user.setter
    def super_user(self, value):
        if isinstance(value, bool):
            self._super_user = value
        else:
            logging.error(f"Invalid value used as super_user: {value}")
            raise ValueError("super_user instance should be a boolean")

    def show_info(self):
        super_user = ""
        if self.super_user is True:
            super_user = "\n  <<SUPER USER>>  "
        return f"""
username : {self.metro_username}
phone_number : {self.phone_number_id.phone_number}
email : {self.email_id.email}{super_user}
"""


# ==================================================================================================================
# ==================================================================================================================


class MetroCard(DBModel):
    TABLE = "card"
    PK = "id"
    card_numbers = []

    def __init__(self, metro_account: MetroAccount, one_trip: bool, credit_card: bool, expirable: bool,
                 expire_date: datetime.date or None, balance: int or float or None):
        self.metro_account_id = metro_account
        self.one_trip = one_trip
        self.credit_card = credit_card
        self.expirable = expirable
        self.expire_date = expire_date
        self.balance = balance
        self.card_number = None
        # db.create(self)

    @staticmethod
    def create(metro_account: MetroAccount, one_trip: bool, credit_card: bool, expirable: bool,
               expire_date: datetime.date or None, balance: int or float or None):
        metro_card = MetroCard(metro_account, one_trip, credit_card, expirable, expire_date, balance)
        with open(f"metro_card_{metro_card.card_number}", "wb") as f:
            pickle.dump(metro_card, f)
        logging.info(f"metro_card with card number: {metro_card.card_number} has been created.")
        return metro_card

    @staticmethod
    def get_obj(card_number):
        with open(f"metro_card_{card_number}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"metro_card with card number: {card_number} has been loaded.")
        return obj

    def edit_expire_date(self, value):
        self.expire_date = value
        with open(f"metro_card_{self.card_number}") as f:
            pickle.dump(self, f)
        db.update(self.expire_date)
        logging.info(f"expire_date has been edited: {value}")

    def deposit(self, value):
        self.balance += value
        with open(f"metro_card_{self.card_number}") as f:
            pickle.dump(self, f)
        db.update(self.balance)
        logging.info(f"expire_date has been edited: {value}")

    @staticmethod
    def delete_card(card_number):
        os.remove(f"metro_card_{card_number}")
        obj = MetroCard.get_obj(card_number)
        db.delete(obj)
        logging.info(f"Metro Card: {card_number} has been Deleted")

    def buy(self, amount):
        self.balance -= amount
        with open(f"metro_card_{self.card_number}") as f:
            pickle.dump(self, f)
        db.update(self.balance)
        logging.info(f"Metro account: {self.metro_account_id.metro_username} has bought card: {self.card_number}")

    def charge(self, amount):
        self.balance += amount
        with open(f"metro_card_{self.card_number}") as f:
            pickle.dump(self, f)
        db.update(self.balance)
        logging.info(f"Metro Card: {self.card_number} has been charged {amount}$")

    @property
    def metro_account_id(self):
        return self._metro_account_id

    @metro_account_id.setter
    def metro_account_id(self, value):
        if isinstance(value, MetroAccount):
            self._metro_account_id = value
        else:
            logging.error(f"Invalid Metro Account: {value}")
            raise ValueError("metro_account_id should be an instance of class MetroAccount")

    @property
    def one_trip(self):
        return self._one_trip

    @one_trip.setter
    def one_trip(self, value):
        if isinstance(value, bool):
            self._one_trip = value
        else:
            logging.error(f"Invalid one_trip value: {value}")
            raise ValueError("one_trip value should be an instance of 'bool'")

    @property
    def credit_card(self):
        return self._credit_card

    @credit_card.setter
    def credit_card(self, value):
        if self.one_trip == value and not isinstance(value, bool):
            logging.error(f"Invalid credit_card value: {value}")
            raise ValueError("more than one card type selected")
        else:
            self._credit_card = value

    @property
    def expirable(self):
        return self._expirable

    @expirable.setter
    def expirable(self, value):
        if self.one_trip == value or self.credit_card == value and not isinstance(value, bool):
            logging.error(f"Invalid expirable value: {value}")
            raise ValueError("more than one card type selected")
        else:
            self._expirable = value

    @property
    def expire_date(self):
        return self._expire_date

    @expire_date.setter
    def expire_date(self, value):
        if self.expirable is False:
            self._expire_date = None
        elif isinstance(value, datetime.datetime):
            self._expire_date = value
        else:
            logging.error(f"Invalid expire_date: {value}")
            raise ValueError("only expirable cards can have expire dates")

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if self.one_trip is True and value != 0:
            logging.error(f"Invalid balance: {value}")
            raise ValueError("one trip cards don't have balance")
        elif value < 0:
            logging.error(f"low on margin on card number: {self.card_number}")
            raise LowMargin("not Enough balance")
        else:
            self._balance = value

    @property
    def card_number(self):
        return self._card_number

    @card_number.setter
    def card_number(self, value):
        first_number = None
        if self.one_trip is True:
            first_number = "1"
        elif self.credit_card is True:
            first_number = "2"
        elif self.expirable is True:
            first_number = "3"

        second_number = random.randint(100, 999)
        self._card_number = f"{first_number}{second_number}"
        self.__class__.card_numbers.append(second_number)

    def show_info(self):
        card_type = ""
        balance = ""
        if self.one_trip is True:
            card_type = "\none_trip"
            balance = ""

        if self.credit_card is True:
            card_type = "\ncredit_card"
            balance = f"\n{self.balance}"

        if self.expirable is True:
            card_type = "\nexpirable"
            balance = f"\n{self.balance}"

        return f"""card_number : {self.card_number}
card_type : {card_type}{balance}"""


# ==================================================================================================================
# ==================================================================================================================


class Trip(DBModel):
    TABLE = "trip"
    PK = "id"
    trip_number_counter = 0

    def __init__(self, metro_account: MetroAccount, card_id: MetroCard, start_date: datetime.datetime,
                 end_date: datetime.datetime, origin, destination, price: int):
        self.metro_account_id = metro_account
        self.card_id = card_id
        self.creation_datetime = datetime.datetime.now()
        self.start_datetime = start_date
        self.end_datetime = end_date
        self.origin = origin
        self.destination = destination
        self.price = price
        self.status = False
        self.model = False
        self.__class__.trip_number_counter += 1
        self.trip_number = self.__class__.trip_number_counter
        # db.create(self)

    @staticmethod
    def create(metro_account: MetroAccount, card_id: MetroCard, start_date: datetime.datetime,
               end_date: datetime.datetime, origin, destination, price: int):
        trip = Trip(metro_account, card_id, start_date, end_date, origin, destination, price)
        with open(f"trip_{trip.trip_number}", "wb") as f:
            pickle.dump(trip, f)
        logging.info(f"trip with trip number: {trip.trip_number} has been created.")
        return trip

    @staticmethod
    def get_obj(trip_number):
        with open(f"trip_{trip_number}", "rb") as f:
            obj = pickle.load(f)
        logging.info(f"trip with trip number: {trip_number} has been loaded.")
        return obj

    def edit_start_datetime(self, value):
        self.start_datetime = value
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.start_datetime)
        logging.info(f"trip's start date: {value} has been edited.")

    def edit_end_datetime(self, value):
        self.end_datetime = value
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.end_datetime)
        logging.info(f"trip's end date: {value} has been edited.")

    def edit_origin(self, value):
        self.origin = value
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.origin)
        logging.info(f"trip's origin: {value} has been edited.")

    def edit_destination(self, value):
        self.destination = value
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.destination)
        logging.info(f"trip's destination: {value} has been edited.")

    def edit_status(self, value):
        self.status = value
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        db.update(self.status)
        logging.info(f"trip's status: {value} has been edited.")

    @staticmethod
    def delete_trip(trip_number):
        os.remove(f"trip_{trip_number}")
        obj = Trip.get_obj(trip_number)
        db.delete(obj)
        logging.info(f"trip with trip number: {trip_number} has been removed.")

    def is_model(self):
        self.model = True
        with open(f"trip_{self.trip_number}", "wb") as f:
            pickle.dump(self, f)
        logging.info(f"trip with trip number: {self.trip_number} has been removed.")

    @property
    def card_id(self):
        return self._card_id

    @card_id.setter
    def card_id(self, value):
        if isinstance(value, MetroCard):
            self._card_id = value
        else:
            logging.error(f"Invalid card: {value}")
            raise ValueError("card_id should be an instance of class MetroCard")

    @property
    def metro_account_id(self):
        return self._metro_account_id

    @metro_account_id.setter
    def metro_account_id(self, value):
        if isinstance(value, MetroAccount):
            self._metro_account_id = value
        else:
            logging.error(f"Invalid metro account: {value}")
            raise ValueError("metro_account_id should be an instance of class MetroAccount")

    @property
    def start_datetime(self):
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, value):
        if value >= self.creation_datetime:
            self._start_datetime = value
        else:
            print(value)
            print(self.creation_datetime)
            logging.error(f"Invalid start_datetime: {value}")
            raise ValueError("the trip cant be started before the purchase")

    @property
    def end_datetime(self):
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, value):
        if value > self.start_datetime:
            self._end_datetime = value
        else:
            logging.error(f"Invalid end_datetime: {value}")
            raise DateError("end date cant be before the start date")

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        if self.end_datetime > datetime.datetime.now():
            if self.start_datetime < datetime.datetime.now():
                if value is False:
                    logging.error(f"Invalid status: {value}")
                    raise ValueError("Wrong status")
        else:
            self.status = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value >= 0:
            self._price = value
        else:
            logging.error(f"Invalid price: {value}")
            raise ValueError("price not valid")

    def show(self):
        return f""" card_number : {self.card_id.card_number}
creation date : {self.creation_datetime}
start date : {self.start_datetime}
end date : {self.end_datetime}
origin : {self.origin}
destination : {self.destination}
price : {self.price}
status : {self.status}
trip number : {self.trip_number}"""
