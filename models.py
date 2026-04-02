import datetime as dt
import random as rd
import os
from dotenv import load_dotenv

load_dotenv()


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

    def withdraw(self, amount: float, input_pin: int, action_id: int):
        if self.check_pin(input_pin) and amount > 0.0 and amount < self.balance:
            self.balance -= amount
            self.record_action(action_id, dt.datetime.now(), amount, "withdraw")
            return "success"
        else:
            return "failed"

    def transaction_out(self, amount: float, input_pin: int, action_id: int):
        return self.withdraw(amount, input_pin, action_id)

    def deposit(self, amount: float, input_pin: int, action_id: int):
        if self.check_pin(input_pin) and amount > 0.0:
            self.balance += amount
            self.record_action(action_id, dt.datetime.now(), amount, "deposit")
            return "success"
        else:
            return "failed"

    def transaction_in(self, amount: float, input_pin: int, action_id: int):
        return self.deposit(amount, input_pin, action_id)

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

    def record_action(self, action_id: int, date_time: dt.datetime, amount: float, type: str):
        if type in {"withdraw", "deposit", "transaction_in", "transaction_out"}:
            self.actions_log.append({
                "action_id": action_id,
                "time": date_time,
                "amount": amount,
                "type": type
            })

    def actions_log_to_dictionary(self):
        actions_log_dictionary = {}
        for action in self.actions_log:
            key = action["action_id"]
            actions_log_dictionary[key] = {
                "time": str(action["time"]),
                "amount": action["amount"],
                "type": action["type"]
                }
        return actions_log_dictionary


class Bank:
    def __init__(self):
        self._accounts: dict[int, Account] = {}

    def create_account(self, name: str, balance: float = 0) -> Account:
        account_id = self._generate_id()
        account = Account(name=name, balance=balance, id=account_id)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: int):
        return self._accounts.get(account_id)

    def is_account_created(self, account_id: int) -> bool:
        return account_id in self._accounts

    def list_all_accounts(self):
        for account_id, account in self._accounts.items():
            print(f"ID: {account_id} | Username: {account.name} | Balance: {account.balance} | Active: {account.is_blocked} | PIN: {account.pin}")

    def transaction_to_from_accounts(self, sender_id: int, receiver_id: int, amount: float):
        if not self.is_account_created(sender_id):
            return False, "sender account not found"
        if not self.is_account_created(receiver_id):
            return False, "receiver account not found"
        sender = self._accounts[sender_id]
        if sender.balance < amount:
            return False, "insufficient balance"
        self._accounts[sender_id].balance -= amount
        self._accounts[receiver_id].balance += amount
        return True, "success"

    def log_in_account(self, account_id: int, pin: int):
        if not self.is_account_created(account_id):
            return False, "account not created"
        account = self._accounts[account_id]
        if account.is_blocked:
            return False, "account suspended"
        if account.check_pin(pin):
            return True, "logged in"
        return False, "incorrect PIN"

    def _generate_id(self) -> int:
        account_id = rd.randint(10000, 99999)
        while account_id in self._accounts:
            account_id = rd.randint(10000, 99999)
        return account_id

    @staticmethod
    def is_admin_pin(entered_password) -> bool:
        return entered_password == os.getenv("ADMIN_SECRET_PASS")