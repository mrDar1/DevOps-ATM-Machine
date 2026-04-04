import models


account1 = models.Account("David Snir",80,222)
print(account1.pin)
print(account1.balance)
if account1.change_pin(input("old pin: "),input("new pin: ")):
    print("pin changed")
else:
    print("pin didnt change")
print(account1.deposit(10,input("[deposit] enter pin: ")))
print(account1.balance)
print(account1.transaction_in(10,"yuval"))
print(account1.balance)
print(account1.withdraw(10,input("[withdraw] enter pin: ")))
print(account1.balance)
print(account1.transaction_out(10000000,input("[transaction_out] enter pin: "),"yuval"))
print(account1.balance)
print(account1.actions_log_to_dictionary())