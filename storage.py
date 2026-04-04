"""here have 2 main functions (as fitussi intructed):
1. save_data(bank) - take Bank object, write to 'data.json'
2. load_data() - read from 'data.json'
problem: json can only work with basic data types as Dict. so we must convert.
the other 2 functions are helper's to convert Bank obj to dict and dict to Bank obj"""

## ! our design - in UI must use "save_data(bank)" after every action.

import json
import datetime as dt
from models import Bank, Account


def _bank_to_dict(bank: Bank) -> dict:
    data = {}
    for account_id, account in bank._accounts.items():
        data[str(account_id)] = {
            "name": account.name,
            "balance": account.balance,
            "pin": account.pin,
            "is_blocked": account.is_blocked,
            "actions_log": account.actions_log_to_dictionary()
        }
    return data


def save_data(bank) -> None:
    """take Bank object, convert to dict, write to 'data.json' """
    data = _bank_to_dict(bank)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)


def _dict_to_bank_object(data_as_dict_object: dict) -> Bank:
    bank = Bank()
    for account_id_str, account_data in data_as_dict_object.items():
        account_id = int(account_id_str)
        account = Account(name=account_data["name"], balance=account_data["balance"], id=account_id)
        account.pin = account_data["pin"]
        account.is_blocked = account_data["is_blocked"]
        account.actions_log = [
            {
                "time": dt.datetime.fromisoformat(action["time"]),
                "amount": action["amount"],
                "type": action["type"],
                "counterparty": action["counterparty"]
            }
            for action in account_data["actions_log"].values()
        ]
        bank._accounts[account_id] = account
    return bank


def load_data() -> Bank:
    """read from 'data.json' as Dict, than convert to Bank object, and return it
    if there is no file, return a new Bank object with empty accounts"""
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data_as_dict_object = json.load(file)
    except FileNotFoundError:
        data_as_dict_object = {}

    data_as_bank_obj = _dict_to_bank_object(data_as_dict_object)
    return data_as_bank_obj
