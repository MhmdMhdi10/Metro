import datetime
import random
import os
import pickle

from Titler.Titler import titler

from Exeptions.models import *

from User.models import User
from User.models import PhoneNumber
from User.models import Email


from Bank.models import Bank, AccountType, BankAccount, CentralBank


from Metro.models import MetroAccount, MetroCard, Trip


user = User.create("M", "M", "1010101010")
phone_number = PhoneNumber.create(user, "09123456789", "IR_MCI")
email = Email.create(user, "mm33007@outlook.com")

central_bank = CentralBank.create("Iran")
bank = Bank.create("the bank", central_bank, "6037")
account_type = AccountType.create(central_bank, "simple", 1)
bank_account = BankAccount.create(bank=bank, user=user, account_type=account_type,
                                  bank_account_number="1234", bank_account_password="1234",
                                  email=email, phone_number=phone_number, balance=10000)

metro_account = MetroAccount.create(user, "MM10", "1234", True, False, email, phone_number)
metro_card = MetroCard.create(metro_account, True, False, False, None, 0)

n = datetime.datetime.now()

metro_trip1 = Trip.create(metro_account, metro_card, datetime.datetime(n.year, n.month, n.day, n.hour, n.minute + 1)
                          , datetime.datetime(2024, 12, 12, 12),
                          "Iran", "USA", 100)


while True:
    while True:
        print(titler("MAIN"))
        print("1.Bank \n2.Metro \n3.Quit")
        terminal_Main = input(">> ").strip()

        while terminal_Main == "1":  # /////////////////////////////////////////////////////////////////// 1.Bank DONE
            print(titler("BANK"))
            print("""1.Login \n2.SignUp \n3.Back""")
            terminal_Bank = input(">> ")

            while terminal_Bank == "1":  # ============================================================== 1.Login DONE
                while True:  # LOGIN BANK
                    print(titler("Login"))
                    bank_login_terminal = input("bank account number: ").strip()  # ---------------->>>> account_number

                    if bank_login_terminal == "cancel":
                        break

                    try:
                        with open(f"bank_account_{bank_login_terminal}", "rb") as f:
                            account: BankAccount = pickle.load(f)
                    except FileNotFoundError:
                        print("account does not exist")
                        break

                    bank_login_terminal = input("bank account password: ")  # -------------------->>> account_password

                    if bank_login_terminal == "cancel":
                        break

                    if not account.bank_account_password == bank_login_terminal:
                        print("wrong password")

                    while account.bank_account_password == bank_login_terminal:  # --------------- Login Complete DONE
                        print(titler(f"Welcome {account.user_id.first_name} {account.user_id.last_name}"))
                        print("1.Show info \n2.edit info \n3.transfer \n4.cash \n5.deposit \n6.Exit")
                        bank_login_terminal2 = input(">> ")
                        if bank_login_terminal2 == "1":  # --------------------------------------------- show info DONE
                            print(titler("Show Info"))
                            print(account.show_info())

                        while bank_login_terminal2 == "2":  # ------------------------------------------ edit info DONE
                            print(titler("Edit Info"))
                            print("1.edit password \n2.edit email \n3.edit phone number \n4.Back")
                            bank_edit_terminal = input(">> ")
                            while bank_edit_terminal == "1":  # ----------------- 1.edit password DONE
                                print(titler("Edit Password"))
                                pass_input = input("current_password : ")
                                if pass_input == "cancel":
                                    break
                                new_pass = input("new pass : ")
                                if new_pass == "cancel":
                                    break
                                new_pass2 = input("new pass repeat : ")
                                if new_pass2 == "cancel":
                                    break

                                try:
                                    account.edit_password(pass_input, new_pass, new_pass2)
                                except WrongPass:
                                    print("current password is not right")
                                    break

                                except PassRepeatError:
                                    print("new passwords doesnt match")
                                    break

                                break

                            while bank_edit_terminal == "2":  # --------------------- 2.edit email DONE
                                print(titler("Edit Email"))
                                new_email = input("new email : ")
                                if new_email == "cancel":
                                    break
                                    try:
                                        account.edit_email(new_email)
                                    except ValueError:
                                        print("email doesnt exist")

                            while bank_edit_terminal == "3":  # -------------- 3.edit phone number DONE
                                print(titler("Edit Phone Number"))
                                new_phone_number = input("new phone_number : ")
                                if new_phone_number == "cancel":
                                    break
                                else:
                                    try:
                                        account.edit_email(new_phone_number)
                                    except ValueError:
                                        print("phone_number doesnt exist")

                            if bank_edit_terminal == "4":  # ------------------------------ 4.Back DONE
                                break

                        while bank_login_terminal2 == "3":  # ------------------------------------------ transfer DONE
                            print(titler("transfer"))
                            cash_terminal = input("destination card number: ")
                            try:
                                destination_account: BankAccount = BankAccount.get_obj(cash_terminal)
                            except FileNotFoundError:
                                print("account doesnt exist")
                                break
                            cash_terminal = input("how much to transfer")

                            try:
                                account.balance -= cash_terminal
                            except ValueError:
                                print("low Margin")
                                break

                            destination_account += cash_terminal

                        while bank_login_terminal2 == "4":  # ---------------------------------------------- cash DONE
                            print(titler("Cash"))
                            cash_terminal = int(input("how much : "))
                            if cash_terminal == 0:
                                break
                            try:
                                account.cash(cash_terminal)
                                break
                            except ValueError:
                                print("write a number")
                            except LowMargin:
                                print("Low Margin")
                                break

                        while bank_login_terminal2 == "5":  # ------------------------------------------- deposit DONE
                            print(titler("Deposit"))
                            cash_terminal = int(input("how much : "))
                            if cash_terminal == 0:
                                break
                            try:
                                account.deposit(cash_terminal)
                                break
                            except ValueError:
                                print("write a number")

                        if bank_login_terminal2 == "6":  # -------------------------------------------------- Exit DONE
                            break

                if bank_login_terminal == "cancel":
                    break

            while terminal_Bank == "2":  # ======================================================== 2.SighUP BANK DONE
                while True:
                    print(titler("SignUP"))
                    bank_signup_terminal = input("Bank number: ")
                    try:
                        bank = Bank.get_obj(bank_signup_terminal)
                    except FileNotFoundError:
                        print("bank doesnt exist")

                    bank_signup_terminal = input("account_type : ")
                    try:
                        account_type = AccountType.get_obj(bank_signup_terminal)
                    except FileNotFoundError:
                        print("account type doesnt exist")

                    bank_account_number = random.randint(1000, 9999)

                    bank_account_password = input("password : ")

                    bank_signup_terminal = input("email: ")
                    try:
                        email = Email.get_obj(bank_signup_terminal)
                    except FileNotFoundError:
                        print("email doesnt exist")

                    bank_signup_terminal = input("phone_number: ")
                    try:
                        phone_number = PhoneNumber.get_obj(bank_signup_terminal)
                    except FileNotFoundError:
                        print("phone number doesnt exist")

                    bank_start_balance = int(input("starting balance: "))

                    try:
                        BankAccount.create(user=user, bank=bank, account_type=account_type,
                                           phone_number=phone_number, email=email,
                                           bank_account_number=bank_account_number,
                                           bank_account_password=bank_account_password, balance=bank_start_balance)
                    except ValueError:
                        print("information not valid")

            if terminal_Bank == "3":  # ------------------------------------------------------------- 3.Back BANK DONE
                break

        while terminal_Main == "2":  # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ 2.Metro
            print(titler("METRO"))
            print("1.Login \n2.SignUp \n3.Exit")

            metro_terminal = input(">> ")

            while metro_terminal == "1":  # ================================================================== 1.Login
                print(titler("Login"))
                username = input("username : ")
                try:
                    metro_account: MetroAccount = MetroAccount.get_obj(username)
                except FileNotFoundError:
                    print("username doesnt exist")
                    break

                password = input("password : ")

                while metro_account.metro_password == password:  # ----------------------------------- Login Complete
                    super_user = ""
                    if metro_account.super_user is True:
                        super_user = "\n4.Management"

                    print(titler("WELCOME"))

                    print(f"1.Profile \n2.Card Service \n3.Trip Service {super_user} \n5.LogOut")

                    metro_login_terminal = input(">> ")

                    while metro_login_terminal == "1":  # ------------------------------------------- Profile
                        print(titler("Profile"))
                        print("1.show info \n2.edit username \n3.edit password \n4.edit email \n5.edit phone number "
                              "\n6.Exit")
                        profile_terminal = input(">> ")
                        if profile_terminal == "1":  # -------------------- 1.show info
                            print(metro_account.show_info())

                        while profile_terminal == "2":  # -------------------- 2.edit username
                            new_username = input("new username : ")
                            if new_username == "cancel":
                                break
                            try:
                                metro_account.edit_username(new_username)
                                break
                            except ExistingObjError:
                                print("username already exists")

                        while profile_terminal == "3":  # -------------------- 3.edit password
                            current_pass = input("current password : ")
                            if current_pass == "cancel":
                                break

                            new_pass = input("new password : ")
                            if new_pass == "cancel":
                                break

                            new_pass2 = input("new password repeat : ")
                            if new_pass2 == "cancel":
                                break

                            try:
                                metro_account.edit_password(current_pass, new_pass, new_pass2)

                            except PassRepeatError:
                                print("new passwords dont match")
                                break

                            except WrongPass:
                                print("current pass is wrong")
                                break

                            except WeakPass:
                                print("new pass is weak")
                                break

                            break

                        while profile_terminal == "4":  # -------------------- 4.edit email
                            new_email = input("new username : ")
                            if new_email == "cancel":
                                break
                            try:
                                new_email = Email.get_obj(new_email)
                            except FileNotFoundError:
                                print("email doesnt exist")

                            metro_account.edit_username(new_email)

                        while profile_terminal == "5":  # -------------------- 5.edit phone number
                            new_phone_number = input("new phone_number : ")
                            if new_phone_number == "cancel":
                                break
                            try:
                                new_phone_number = PhoneNumber.get_obj(new_phone_number)
                            except FileNotFoundError:
                                print("phone_number doesnt exist")

                            metro_account.edit_username(new_phone_number)

                        if profile_terminal == "6":
                            break

                    if metro_login_terminal == "2":  # -------------------------------------- Card Service
                        print(titler("Card Service"))
                        print("1.My Cards \n2.buy card \n3.charge card \n4.Exit")
                        metro_login_terminal = input(">> ")

                        if metro_login_terminal == "1":  # ----------------- 1.My Cards
                            print(titler("My Cards"))
                            cards = []
                            for card_number in MetroCard.card_numbers:
                                card: MetroCard = MetroCard.get_obj(card_number)
                                if card.metro_account_id == metro_account:
                                    cards.append(card)
                            for i in cards:
                                print(i.show_info())

                        while metro_login_terminal == "2":  # ----------------- 2.buy card
                            print(titler("Buy Card"))
                            print("1.Expirable \n2.credit_card \n3.one_trip")

                            price = 20
                            now = datetime.date.today()
                            expire_date = datetime.date(now.year + 1, now.month, now.day)

                            buy_card_terminal = input(">> ")
                            if buy_card_terminal == "1":
                                Expirable = True
                                credit_card = False
                                one_trip = False

                            if buy_card_terminal == "2":
                                expire_date = None
                                Expirable = False
                                credit_card = True
                                one_trip = False

                            if buy_card_terminal == "3":
                                expire_date = None
                                Expirable = False
                                credit_card = False
                                one_trip = True

                            bank_account_number = input("bank account number : ")
                            bank_account: BankAccount = BankAccount.get_obj(bank_account_number)
                            bank_account_password = input("bank account password : ")

                            if bank_account.bank_account_password == bank_account_password:
                                bank_account.cash(price)
                                MetroCard.create(metro_account, one_trip, credit_card, expirable, expire_date, 0)

                            MetroCard.create(metro_account, one_trip, credit_card, Expirable, expire_date, price)

                        while metro_login_terminal == "3":  # ----------------- 3.charge card
                            card_number = input("card_number : ")
                            try:
                                card = MetroCard.get_obj(card_number)
                            except FileNotFoundError:
                                print("card doesnt exist")
                                break

                            if card.one_trip is True:
                                print("you cant charge a one_trip card")

                            how_much = float(input("how much : "))

                            bank_account_number = input("bank account password : ")
                            try:
                                bank_account = BankAccount.get_obj(bank_account_number)
                            except FileNotFoundError:
                                print("account doesnt exist")
                                break

                            bank_account_password = input("bank account password : ")

                            if bank_account.bank_account_password == bank_account_password:
                                bank_account.cash(how_much)
                                card.charge(how_much)
                                break

                        if metro_login_terminal == "4":  # ----------------- 4.Exit
                            break

                    while metro_login_terminal == "3":  # -------------------------------------- Trip Service
                        print(titler("Trip Service"))
                        print("1.my trips \n2.Buy trips")
                        trips_terminal = input(">> ")

                        if trips_terminal == "1":  # --------------- my trips
                            for i in range(Trip.trip_number_counter + 1):
                                trip = trip.get_obj(i)
                                print(trip.show())
                                print(titler(""))

                        while trips_terminal == "2":  # --------------- buy trips
                            print("trips_list 1 2 3 4 5 .....")
                            x = input(">> ")  # trips will be for a superuser and the data will be copied and a new
                            break  # trip will be made for the metro account that is logged in

                    if metro_login_terminal == "4" and metro_account.super_user is True:  # ---- Management
                        print(titler("Management (ADMIN PANEL)"))
                        print("1.get user \n2.get trip \n3.get card")
                        management_terminal = input(">> ")
                        while management_terminal == "1":
                            metro_account_username = input("metro_account_username : ")
                            metro_account = MetroAccount.get_obj(metro_account_username)
                            print(metro_account.show_info())

                        while management_terminal == "2":
                            trip_number = input("trip_number : ")

                        while management_terminal == "3":
                            pass

                    if metro_login_terminal == "5":  # -------------------------------------------- LogOut
                        break

            while metro_terminal == "2":  # ============================================================ 2.SignUp DONE
                print(titler("SignUP"))

                username = input("username : ")
                password = input("password")

                phone_number = input("phone_number : ")
                try:
                    phone_number = PhoneNumber.get_obj(phone_number)
                except FileNotFoundError:
                    print("phone_number doesnt exist")
                    break

                email = input("email : ")
                try:
                    email = Email.get_obj(email)
                except FileNotFoundError:
                    print("email doesnt exist")
                    break
                try:
                    MetroAccount.create(user=user, metro_username=username, metro_password=password, email=email,
                                        phone_number=phone_number, banned=False, super_user=False)
                except ValueError:
                    print("wrong inputs")
                    break

                except ExistingObjError:
                    print("username already exists")
                    break

                except WeakPass:
                    print("password is weak")
                    break

                break

            if metro_terminal == "3":  # ================================================================= 3.Exit DONE
                break

        while terminal_Main == "3":  # ------------------------------------------------------------------- 3.Quit DONE
            quit()
