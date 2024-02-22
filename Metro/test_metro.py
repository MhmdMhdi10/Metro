import os
import logging

import pytest
from Exeptions.models import *
from models import MetroAccount, MetroCard, Trip
from User.models import User, PhoneNumber, Email


class MetroTest:
    @pytest.fixture
    def setup(self):
        self.user = User.create("John", "Doe", "1234567890")
        self.email = Email.create(self.user, "wer@gmail.com")
        self.phone_number = PhoneNumber.create(self.user, "09304116941", "IR")
        self.metro = MetroAccount.create(self.user, 'usrnm', "1234", False, banned=False,
                                         email=self.email, phone_number=self.phone_number)

        yield 'setup'

    def test_metro_account_creation(self, setup):
        metro = MetroAccount.get_obj('1234')
        print(metro)
        assert metro.metro_username == 'usrnm'
        assert metro.metro_password == '1234'
        assert metro.super_user is False
        assert metro.banned is False
        assert metro.user_id == self.user
        assert metro.email_id == self.email
        assert metro.phone_number_id == self.phone_number
        with pytest.raises(ValueError):
            metro.username = 1234
        with pytest.raises(ValueError):
            metro.password = 1234
        with pytest.raises(ValueError):
            metro.is_admin = '1234'
        with pytest.raises(ValueError):
            metro.is_banned = '1234'
        with pytest.raises(ValueError):
            metro.user_id = '1234'
        with pytest.raises(ValueError):
            metro.email = '1234'
        with pytest.raises(ValueError):
            metro.phone_number = '1234'

    def test_metro_card_creation(self, setup):
        metro_card = MetroCard.create(self.metro, 10000)
        assert metro_card.metro_account_id == self.metro
        assert metro_card.balance == 10000
        with pytest.raises(ValueError):
            metro_card.metro_account_id = '1234'
        with pytest.raises(ValueError):
            metro_card.balance = '1234'

    def test_trip_creation(self, setup):
        metro_card = MetroCard.create(self.metro, 10000)
        trip = Trip.create(metro_card, 1000)
        assert trip.metro_card_id == metro_card
        assert trip.fare == 1000
        with pytest.raises(ValueError):
            trip.metro_card_id = '1234'
        with pytest.raises(ValueError):
            trip.fare = '1234'


