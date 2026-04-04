import tkinter as tk
import styles
import ui
from models import Bank




bank = Bank()
bank.create_account("David")
bank.list_all_accounts()

def login(id, pin):
    global bank
    if bank.is_account_created(id):
        bank.log_in_account(id,pin)



app = ui.ATMApp(bank=bank)
app.mainloop()
