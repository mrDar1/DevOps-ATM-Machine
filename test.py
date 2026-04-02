from models import Account


account1 = Account("David Snir",80,222)
print(account1.pin)
print(account1.balance)
if account1.change_pin(int(input("old pin: ")),int(input("new pin: "))):
    print("pin changed")
else:
    print("pin didnt change")
print(account1.deposit(10,int(input("[deposit] enter pin: "))))
print(account1.balance)
print(account1.transaction_in(10,int(input("[transaction_in] enter pin: ")),"yuval"))
print(account1.balance)
print(account1.withdraw(10,int(input("[withdraw] enter pin: "))))
print(account1.balance)
print(account1.transaction_out(10000000,int(input("[transaction_out] enter pin: ")),"yuval"))
print(account1.balance)
print(account1.actions_log_to_dictionary())