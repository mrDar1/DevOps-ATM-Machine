import tkinter as tk
import styles
import ui
from models import Bank, Account


bank = Bank()

# * enter testing values -----finish * #
# * enter testing values -----finish * #

bank.create_account("David", 1000)
account = bank._get_account_by_name("David")
account.withdraw(10, account.pin)
account.deposit(20.2, account.pin)
account.transaction_in(1000, "yuval")
account.transaction_out(88, account.pin, "yuval")
bank.list_all_accounts()

# * enter testing values -----finish * #
# * enter testing values -----finish * #


app = ui.ATMApp(bank=bank)
app.mainloop()
