import pytest
import os
import pickle
from models import User


class TestUser:

    def test_user_creation(self):
        first_name = "John"
        last_name = "Doe"
        national_id = "1234567890"
        user = User.create(first_name, last_name, national_id)

        assert os.path.exists(f"User_{national_id}")
        with open(f"User_{national_id}", "rb") as f:
            obj = pickle.load(f)
            assert obj.first_name == first_name
            assert obj.last_name == last_name
            assert obj.national_id == national_id

        os.remove(f"User_{national_id}")

    def test_user_get_obj(self):
        first_name = "John"
        last_name = "Doe"
        national_id = "1234567890"
        user = User.create(first_name, last_name, national_id)

        obj = User.get_obj(national_id)
        assert obj.first_name == first_name
        assert obj.last_name == last_name
        assert obj.national_id == national_id

        os.remove(f"User_{national_id}")

    def test_first_name_validation(self):
        with pytest.raises(ValueError, match="name should only have alphabets"):
            user = User("John1", "Doe", "1234567890")

    def test_last_name_validation(self):
        with pytest.raises(ValueError, match="name should only have alphabets"):
            user = User("John", "Doe1", "1234567890")

    def test_national_id_validation(self):
        with pytest.raises(ValueError, match="national id is not valid"):
            user = User("John", "Doe", "123456789")
        with pytest.raises(ValueError, match="national id is not valid"):
            user = User("John", "Doe", "123456789a")
