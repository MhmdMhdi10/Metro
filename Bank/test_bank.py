import pytest
import os
import pickle
from models import Bank, CentralBank, AccountType, BankAccount
from User.models import User, Email, PhoneNumber


class TestBank:

    @pytest.fixture
    def setup(self):
        self.central_bank = CentralBank.create("IRAN")
        self.bank = Bank.create("Mellat", self.central_bank, '1234')
        self.account_type = AccountType.create(self.central_bank, "one", 100)
        self.user = User.create("John", "Doe", "1234567890")
        self.email = Email.create(self.user, "wer@gmail.com")
        self.phone_number = PhoneNumber.create(self.user, "09304116941", "IR")
        self.bank_account = BankAccount.create(self.bank, self.user, self.account_type, 2432, '1000',
                                               self.email, self.phone_number, 10000)
        yield 'setup'

    def test_bank_creation(self, setup):
        central_bank = CentralBank.get_obj("IRAN")
        bank = Bank.get_obj("1234")

        assert bank.bank_name == "Mellat"
        with pytest.raises(ValueError):
            bank.central_bank_id = 'yoyo'
