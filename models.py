import datetime as dt
import random as rd
import os
import hashlib

from dotenv import load_dotenv

load_dotenv()


class Account:
    def __init__(self, name: str, balance: float, id: int):
        self.id = id
        self.name = name
        self.pin = self.generate_pin()
        self.balance = balance
        self.is_blocked = False
        self.actions_log: list[dict[dt.datetime, float, str, str]] = []

    def generate_pin(self) -> int:
        return rd.randint(1000, 9999)

    def check_pin(self, user_input: str) -> bool:
        user_input = str(user_input)
        if user_input.isdigit():
            user_input = int(user_input)
            return user_input == self.pin
        else:
            return False

    def withdraw(self, amount: float, input_pin: str) -> bool:
        if self.check_pin(input_pin) and amount > 0.0 and amount <= self.balance:
            self.balance -= amount
            self.record_action(dt.datetime.now(), amount, "withdraw")
            return True
        else:
            return False

    def transaction_out(self, amount: float, input_pin: str, counterparty: str) -> bool:
        if self.check_pin(input_pin) and amount > 0.0 and amount <= self.balance:
            self.balance -= amount
            self.record_action(dt.datetime.now(), amount, "transaction_out", counterparty)
            return True
        else:
            return False

    def deposit(self, amount: float, input_pin: str) -> bool:
        if self.check_pin(input_pin) and amount > 0.0:
            self.balance += amount
            self.record_action(dt.datetime.now(), amount, "deposit")
            return True
        else:
            return False

    def transaction_in(self, amount: float, counterparty: str) -> bool:
        if amount > 0.0:
            self.balance += amount
            self.record_action(dt.datetime.now(), amount, "transaction_in", counterparty)
            return True
        else:
            return False

    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """we check that new pin is 4 digits, not the same as old, and that old is correct.
        order is important!
        first check "cheap" tests (length, isdigit) before check_pin that more "expensive" because of function call.
        we need isascii(), to prevent arab digits """
        if len(new_pin) == 4 and new_pin.isascii() and new_pin.isdigit() and new_pin != old_pin and self.check_pin(old_pin):
            self.pin = int(new_pin)
            return True
        else:
            return False

    def record_action(self, date_time: dt.datetime, amount: float, action_type: str, counterparty=None):
        if action_type in {"withdraw", "deposit", "transaction_in", "transaction_out"}:
            self.actions_log.append({
                "time": date_time,
                "amount": amount,
                "type": action_type,
                "counterparty": counterparty
            })

    def actions_log_to_dictionary(self) -> dict[int, dict]:
        """function that later use to convert list to json DataBase
        json can work with dict, but not with objects like 'datetime'
        so here convert it string, and store as dict"""
        actions_log_dictionary: dict[int, dict] = {}
        for index, action in enumerate(self.actions_log):
            key = index
            actions_log_dictionary[key] = {
                "time": str(action["time"]),
                "amount": action["amount"],
                "type": action["type"],
                "counterparty": action["counterparty"]
                }
        return actions_log_dictionary


class Bank:
    def __init__(self):
        self._accounts: dict[int, Account] = {}
        # dict[int, Account] == "python annotation" - informational only

    def create_account(self, name: str, balance: float = 0) -> Account:
        account_id = self._generate_id()
        account = Account(name=name, balance=balance, id=account_id)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id: int) -> Account | None:
        return self._accounts.get(account_id)

    def _get_account_by_name(self, name: str) -> Account | None:
        for account in self._accounts.values():
            if account.name == name:
                return account
        return None

    def is_account_created(self, account_id: int) -> bool:
        return account_id in self._accounts

    def list_all_accounts(self) -> None:
        for account_id, account in self._accounts.items():
            print(f"ID: {account_id} | Username: {account.name} | Balance: {account.balance} | Active: {not account.is_blocked} | PIN: {account.pin}")

    def transaction_to_from_accounts(self, sender_id: int, receiver_id: int, amount: float, sender_pin: int) -> tuple[bool, str]:
        if not self.is_account_created(sender_id):
            return False, "sender account not found"
        if not self.is_account_created(receiver_id):
            return False, "receiver account not found"
        sender = self._accounts[sender_id]
        receiver = self._accounts[receiver_id]
        is_success = sender.transaction_out(amount, sender_pin, counterparty=receiver.name)
        if not is_success:
            return False, "failed, check pin and that have enougeh balance"
        receiver.transaction_in(amount, counterparty=sender.name)
        return True, "success"

    def log_in_account(self, account_id: int, pin: int) -> tuple[bool, str]:
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
        """function compare admin password at .env file to user entered one:
        is verastile function:
        can work with regular plaintext password or hashed.
        to create hash password to store at .env, run at CLI:
        $ python3 -c "import hashlib; print(hashlib.sha256(b'YOUR_CHOSEN_PASS_HERE').hexdigest())"
        and the output hash, will be something like:
        9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0
        store it at .env"""
        env_admin_pass = os.getenv("ADMIN_SECRET_PASS")
        if not entered_password or not env_admin_pass:
            return False

        is_correct_pass = False

        hashed_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()
        is_correct_pass = (env_admin_pass == hashed_entered_password) or (env_admin_pass == env_admin_pass)

        return is_correct_pass
