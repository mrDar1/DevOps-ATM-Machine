import random
import os
from dotenv import load_dotenv

load_dotenv()


class Account:
    def __init__(self, account_id, username, balance=0, pin=None):
        self.account_id = account_id
        self.username = username
        self.balance = balance
        self.is_active = True
        self.history = []
        self.pin = pin


class Bank(Account):
    accounts = {}

    def __init__(self, username, balance=0):
        super().__init__(self.create_account_id(), username, balance)
        Bank.accounts[self.account_id] = self

    @classmethod
    def create_account_id(cls):
        account_id = random.randint(10000, 99999)
        while account_id in cls.accounts:
            account_id = random.randint(10000, 99999)
        return account_id

    @classmethod
    def is_account_created(cls, account_id):
        return account_id in cls.accounts

    @classmethod
    def list_all_accounts(cls):
        for account_id, account in cls.accounts.items():
            print(f"ID: {account_id} | Username: {account.username} | Balance: {account.balance} | Active: {account.is_active} | PIN: {account.pin}")

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


