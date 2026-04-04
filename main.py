import tkinter as tk
from tkinter import ttk, messagebox
from storage import load_data

bank = load_data()

root = tk.Tk()
root.title("David & Yuval ©")  # window upper title
root.geometry("390x844")  # iPhone 14 portrait

# * UI DESIGN of 'Log In' screen - no logic * #
# * UI DESIGN of 'Log In' screen - no logic * #
# * UI DESIGN of 'Log In' screen - no logic * #

# for dark background
root.configure(bg="#1e1e1e")
style = ttk.Style()
style.theme_use("clam")  # required for color overrides
style.configure("TButton", background="#3c3c3c", foreground="#ffffff")
style.configure("TLabel",  background="#1e1e1e", foreground="#ffffff")
# for dark background - end.

# big title:
title_label = tk.Label(root, text="ATM machine", bg="#1e1e1e", fg="#ffffff", font=("Arial", 16, "bold"))
title_label.place(relx=0.5, rely=0.05, anchor="center")

# account ID entry:
account_label = tk.Label(root, text="Account ID", bg="#1e1e1e", fg="#aaaaaa", font=("Arial", 11))
account_label.place(relx=0.5, rely=0.35, anchor="center")
account_entry = tk.Entry(root, width=28, bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
                         relief="flat", font=("Arial", 13))
account_entry.place(relx=0.5, rely=0.41, anchor="center")

# PIN entry (hidden):
pin_label = tk.Label(root, text="PIN", bg="#1e1e1e", fg="#aaaaaa", font=("Arial", 11))
pin_label.place(relx=0.5, rely=0.50, anchor="center")
pin_entry = tk.Entry(root, width=28, show="●", bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
                     relief="flat", font=("Arial", 13))
pin_entry.place(relx=0.5, rely=0.56, anchor="center")

# Log In button:
login_button = tk.Button(root, text="Log In", width=25,
                         bg="#3c3c3c", fg="#ffffff", activebackground="#555555")
login_button.place(relx=0.5, rely=0.65, anchor="center")

# Admin Zone button:
admin_button = tk.Button(root, text="Admin Zone", width=25,
                         bg="#3c3c3c", fg="#ffffff", activebackground="#555555")
admin_button.place(relx=0.5, rely=0.72, anchor="center")

# Exit button:
button = tk.Button(root, text="Exit", width=25, command=root.destroy,
                   bg="#3c3c3c", fg="#ffffff", activebackground="#555555")
button.place(relx=0.5, rely=0.79, anchor="center")

# * UI DESIGN of 'Log In' screen - no logic -----finish * #
# * UI DESIGN of 'Log In' screen - no logic -----finish * #
# * UI DESIGN of 'Log In' screen - no logic -----finish * #


# * Logic of 'Login' screen * #
# * Logic of 'Login' screen * #
# * Logic of 'Login' screen * #


def handle_login():
    account_id_str = account_entry.get()
    pin_str = pin_entry.get()

    try:
        account_id = int(account_id_str)
        pin = int(pin_str)
    except ValueError:
        messagebox.showerror("Login Failed", "Account ID and PIN must be numbers")
        return

    success, message = bank.log_in_account(account_id, pin)
    if success:
        show_user_menu(account_id)
    else:
        messagebox.showerror("Login Failed", message)


login_button.config(command=handle_login)


# * Logic of 'Login' screen -----finish * #
# * Logic of 'Login' screen -----finish * #
# * Logic of 'Login' screen -----finish * #


# * UI DESIGN of 'user Menu' screen - no logic * #
# * UI DESIGN of 'user Menu' screen - no logic * #
# * UI DESIGN of 'user Menu' screen - no logic * #


def show_user_menu(account_id):
    clear_screen()

    tk.Label(root, text="User Menu", bg="#1e1e1e", fg="#ffffff",
             font=("Arial", 16, "bold")).place(relx=0.5, rely=0.1, anchor="center")
    tk.Label(root, text=f"Account: {account_id}", bg="#1e1e1e", fg="#aaaaaa",
             font=("Arial", 11)).place(relx=0.5, rely=0.2, anchor="center")

    tk.Button(root, text="Log Out", width=25, bg="#3c3c3c", fg="#ffffff",
              activebackground="#555555", command=root.destroy).place(relx=0.5, rely=0.85, anchor="center")
# * UI DESIGN of 'user Menu' screen - no logic -----finish * #
# * UI DESIGN of 'user Menu' screen - no logic -----finish * #
# * UI DESIGN of 'user Menu' screen - no logic -----finish * #


def clear_screen():
    """we use single-window design, so to navigate to new screen must clear it first"""
    for widget in root.winfo_children():
        widget.destroy()


root.mainloop()
