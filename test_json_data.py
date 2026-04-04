"""use website:
https://jsonformatter.curiousconcept.com/#
copy the json file there and see it in a readable way."""

from storage import save_data, load_data
from models import Bank

ACCOUNTS = [
    ("metushelah-1", 1000),
    ("metushelah-2", 2000),
    ("metushelah-3", 3000),
    ("metushelah-4", 4000),
    ("metushelah-5", 5000),
    ("metushelah-6", 6000),
    ("metushelah-7", 7000),
    ("metushelah-8", 8000),
    ("metushelah-9", 9000),
    ("metushelah-10", 10000),
]


def init_test_with10_people_data():
    bank = Bank()

    for name, balance in ACCOUNTS:
        bank.create_account(name=name, balance=balance)

    save_data(bank)
    print("Test data written to data.json")


def test_load_data():
    bank = load_data()
    assert len(bank._accounts) == 10, f"Expected 10 accounts, got {len(bank._accounts)}"
    expected = {name: balance for name, balance in ACCOUNTS}
    for account in bank._accounts.values():
        assert account.name in expected, f"Unexpected account name: {account.name}"
        assert account.balance == expected[account.name], f"Wrong balance for {account.name}"
    print("test_load_data passed: loaded 10 accounts with correct names and balances")


def test_metushelah_1_withdraw():
    bank = load_data()
    account = bank._get_account_by_name("metushelah-1")
    success = account.withdraw(1000, account.pin)
    assert success, "withdraw should succeed"
    assert account.balance == 0, f"Expected balance 0, got {account.balance}"
    save_data(bank)
    print("test_metushelah_1_withdraw passed: balance is 0 after withdrawing 1000")


def test_metushelah_2_deposit():
    bank = load_data()
    account = bank._get_account_by_name("metushelah-2")
    success = account.deposit(1000, account.pin)
    assert success, "deposit should succeed"
    assert account.balance == 3000, f"Expected balance 3000, got {account.balance}"
    save_data(bank)
    print("test_metushelah_2_deposit passed: balance is 3000 after depositing 1000")


def test_metushelah_3_deposit_and_withdraw():
    bank = load_data()
    account = bank._get_account_by_name("metushelah-3")
    success_deposit = account.deposit(1000, account.pin)
    assert success_deposit, "deposit should succeed"
    assert account.balance == 4000, f"Expected balance 4000 after deposit, got {account.balance}"
    success_withdraw = account.withdraw(1000, account.pin)
    assert success_withdraw, "withdraw should succeed"
    assert account.balance == 3000, f"Expected balance 3000 after withdraw, got {account.balance}"
    save_data(bank)
    print("test_metushelah_3_deposit_and_withdraw passed: balance is 3000 after deposit then withdraw")


def test_metushelah_4_transfer_to_metushelah_5():
    bank = load_data()
    sender = bank._get_account_by_name("metushelah-4")
    receiver = bank._get_account_by_name("metushelah-5")
    success, msg = bank.transaction_to_from_accounts(
        sender_id=sender.id, receiver_id=receiver.id, amount=4000, sender_pin=sender.pin
    )
    assert success, f"transfer should succeed, got: {msg}"
    assert sender.balance == 0, f"Expected sender balance 0, got {sender.balance}"
    assert receiver.balance == 9000, f"Expected receiver balance 9000, got {receiver.balance}"
    save_data(bank)
    print("test_metushelah_4_transfer_to_metushelah_5 passed: sender balance 0, receiver balance 9000")


def test_metushelah_4_transfer_to_self():
    bank = load_data()
    account = bank._get_account_by_name("metushelah-4")
    success, msg = bank.transaction_to_from_accounts(
        sender_id=account.id, receiver_id=account.id, amount=4000, sender_pin=account.pin
    )
    assert success, f"transfer should succeed, got: {msg}"
    assert account.balance == 4000, f"Expected balance 4000 after self-transfer, got {account.balance}"
    save_data(bank)
    print("test_metushelah_4_transfer_to_self passed: balance is 4000 after transferring 4000 to self")


if __name__ == "__main__":
    init_test_with10_people_data()
    test_load_data()
    test_metushelah_1_withdraw()
    test_metushelah_2_deposit()
    test_metushelah_3_deposit_and_withdraw()
    test_metushelah_4_transfer_to_self()
    test_metushelah_4_transfer_to_metushelah_5()
