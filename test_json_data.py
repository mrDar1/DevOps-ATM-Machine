from storage import save_data
from models import Bank, Account


def init_test_data():
    bank = Bank()

    for account_id, name, balance in [
        (1, "metushelah-1", 1000),
        (2, "metushelah-2", 2000),
        (3, "metushelah-3", 3000),
        (4, "metushelah-4", 4000),
        (5, "metushelah-5", 5000),
        (6, "metushelah-6", 6000),
        (7, "metushelah-7", 7000),
        (8, "metushelah-8", 8000),
        (9, "metushelah-9", 9000),
        (10, "metushelah-10", 10000),
    ]:
        account = Account(name=name, balance=balance, id=account_id)
        bank._accounts[account_id] = account

    save_data(bank)
    print("Test data written to data.json")


if __name__ == "__main__":
    init_test_data()
