import datetime as dt
import random as rd
import os
# from dotenv import load_dotenv

# load_dotenv()


class Account:
    def __init__(self, name: str, balance: float, id: int):
        self.id = id
        self.name = name
        self.pin = self.generate_pin()
        self.balance = balance
        self.is_blocked = False
        self.actions_log = []


    # def generate_id():
    #     pass

    def generate_pin(self):
        return rd.randint(1000, 9999)

    def check_pin(self, user_input: int):
        return user_input == self.pin

    def withdraw(self, amount: float, input_pin: int):
        if self.check_pin(input_pin) and amount > 0.0 and amount < self.balance:
            self.balance -= amount
            self.record_action(dt.datetime.now(), amount, "withdraw")
            return "success"
        else:
            return "failed"

    def transaction_out(self, amount: float, input_pin: int):
        return self.withdraw(amount, input_pin, )

    def deposit(self, amount: float, input_pin: int):
        if self.check_pin(input_pin) and amount > 0.0:
            self.balance += amount
            self.record_action(dt.datetime.now(), amount, "deposit")
            return "success"
        else:
            return "failed"

    def transaction_in(self, amount: float, input_pin: int):
        return self.deposit(amount, input_pin)

    def change_pin(self, old_pin: int, new_pin: int):
        if self.check_pin(old_pin):
            self.pin = new_pin
            return "success"
        else:
            return "failed"

    # def block_account(self):
    #     self.is_blocked = True

    # def unblock_account(self):
    #     self.is_blocked = False

    def record_action(self, date_time: dt.datetime, amount: float, type: str):
        if type in {"withdraw", "deposit", "transaction_in", "transaction_out"}:
            self.actions_log.append({
                "time": date_time,
                "amount": amount,
                "type": type
            })

    def actions_log_to_dictionary(self):
        actions_log_dictionary = {}
        for index, action in enumerate(self.actions_log):
            key = index
            actions_log_dictionary[key] = {
                "time": str(action["time"]),
                "amount": action["amount"],
                "type": action["type"]
                }
        return actions_log_dictionary


class Bank(Account):
    accounts = {}

    def __init__(self, username, balance=0):
        super().__init__(self.create_account_id(), username, balance)
        Bank.accounts[self.id] = self

    @classmethod
    def create_account_id(cls):
        account_id = rd.randint(10000, 99999)
        while account_id in cls.accounts:
            account_id = rd.randint(10000, 99999)
        return account_id

    @classmethod
    def is_account_created(cls, account_id):
        return account_id in cls.accounts

    @classmethod
    def list_all_accounts(cls):
        for account_id, account in cls.accounts.items():
            print(f"ID: {account_id} | Username: {account.name} | Balance: {account.balance} | Active: {account.is_blocked} | PIN: {account.pin}")

    @staticmethod
    def is_admin_pin(entered_password):
        return entered_password == os.getenv("ADMIN_SECRET_PASS")

    @classmethod
    def transaction_to_from_accounts(cls, sender_id, receiver_id, amount):
        if not cls.is_account_created(sender_id):
            return False, "sender account not found"
        if not cls.is_account_created(receiver_id):
            return False, "receiver account not found"
        sender = cls.accounts[sender_id]
        if sender.balance < amount:
            return False, "insufficient balance"
        cls.accounts[sender_id].balance -= amount
        cls.accounts[receiver_id].balance += amount
        return True

    @classmethod
    def log_in_account(cls, account_id, pin):
        if not cls.is_account_created(account_id):
            return False, "account not created"
        account = cls.accounts[account_id]
        if not account.is_active:
            return False, "account suspend"
        if pin == account.pin:
            return True
        return False, "incorrect PIN"