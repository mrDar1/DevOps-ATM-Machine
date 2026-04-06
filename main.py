"""2 options for UI: David and Dar, uncomment your choice and comment the other one"""
# * dar UI
# import ui_dar
# ui_dar.ATMApp().run()


# * David's UI
import storage
import ui

bank = storage.load_data()
ui.ATMApp(bank).mainloop()
