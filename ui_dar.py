import tkinter as tk
from tkinter import ttk, messagebox
from storage import load_data


class ATMApp:
    def __init__(self):
        self.bank = load_data()

        # * shared UI DESIGN for all screens * #
        self.root = tk.Tk()
        self.root.title("David & Yuval © ATM")  # window upper title
        self.root.geometry("390x844")  # iPhone 14 portrait

        # for dark background
        self.root.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("clam")  # required for color overrides
        style.configure("TButton", background="#3c3c3c", foreground="#ffffff")
        style.configure("TLabel",  background="#1e1e1e", foreground="#ffffff")
        # for dark background - end.
        # * shared UI DESIGN for all screens --- finish * #

    # * UI DESIGN + Logic of 'Log In' screen * #
    def show_login_screen(self):
        self.clear_screen()

        # big title:
        tk.Label(self.root, text="ATM machine", bg="#1e1e1e", fg="#ffffff",
                 font=("Arial", 16, "bold")).place(relx=0.5, rely=0.05, anchor="center")

        # account ID entry:
        tk.Label(self.root, text="Account ID", bg="#1e1e1e", fg="#aaaaaa",
                 font=("Arial", 11)).place(relx=0.5, rely=0.35, anchor="center")
        account_entry = tk.Entry(self.root, width=28, bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
                                 relief="flat", font=("Arial", 13))
        account_entry.place(relx=0.5, rely=0.41, anchor="center")

        # PIN entry (hidden):
        tk.Label(self.root, text="PIN", bg="#1e1e1e", fg="#aaaaaa",
                 font=("Arial", 11)).place(relx=0.5, rely=0.50, anchor="center")
        pin_entry = tk.Entry(self.root, width=28, show="●", bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff",
                             relief="flat", font=("Arial", 13))
        pin_entry.place(relx=0.5, rely=0.56, anchor="center")

        def handle_login():
            account_id_str = account_entry.get()
            pin_str = pin_entry.get()

            try:
                account_id = int(account_id_str)
                pin = int(pin_str)
            except ValueError:
                messagebox.showerror("Login Failed", "Account ID and PIN must be numbers")
                return

            success, message = self.bank.log_in_account(account_id, pin)
            if success:
                self.show_user_menu(account_id)
            else:
                messagebox.showerror("Login Failed", message)

        # Log In button:
        tk.Button(self.root, text="Log In", width=25, bg="#3c3c3c", fg="#ffffff",
                  activebackground="#555555", command=handle_login).place(relx=0.5, rely=0.65, anchor="center")

        # Admin Zone button:
        tk.Button(self.root, text="Admin Zone", width=25, bg="#3c3c3c", fg="#ffffff",
                  activebackground="#555555").place(relx=0.5, rely=0.72, anchor="center")

        # Exit button:
        tk.Button(self.root, text="Exit", width=25, command=self.root.destroy,
                  bg="#3c3c3c", fg="#ffffff", activebackground="#555555").place(relx=0.5, rely=0.79, anchor="center")

    # * UI DESIGN + Logic of 'Log In' screen -----finish * #

    # * UI DESIGN of 'user Menu' screen - no logic * #
    def show_user_menu(self, account_id):
        self.clear_screen()
        account = self.bank.get_account(account_id)

        # --- info frame ---
        info_frame = tk.Frame(self.root, bg="#2e2e2e", bd=0)
        info_frame.place(relx=0.5, rely=0.13, anchor="center", width=320)

        tk.Label(info_frame, text=account.name, bg="#2e2e2e", fg="#ffffff",
                 font=("Arial", 15, "bold")).pack(pady=(12, 2))
        tk.Label(info_frame, text=f"ID: {account.id}", bg="#2e2e2e", fg="#aaaaaa",
                 font=("Arial", 11)).pack()
        tk.Label(info_frame, text=f"Balance: ${account.balance:,.2f}", bg="#2e2e2e", fg="#4caf50",
                 font=("Arial", 13, "bold")).pack(pady=(4, 12))

        # --- buttons frame ---
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.place(relx=0.5, rely=0.57, anchor="center")

        btn_cfg = dict(width=25, bg="#3c3c3c", fg="#ffffff",
                       activebackground="#555555", font=("Arial", 11), relief="flat")

        tk.Button(btn_frame, text="Deposit",    **btn_cfg).pack(pady=5)
        tk.Button(btn_frame, text="Withdraw",   **btn_cfg).pack(pady=5)
        tk.Button(btn_frame, text="Send",       **btn_cfg).pack(pady=5)
        tk.Button(btn_frame, text="History",    **btn_cfg).pack(pady=5)
        tk.Button(btn_frame, text="Change PIN", **btn_cfg).pack(pady=5)
        tk.Button(btn_frame, text="Exit entire App", command=self.root.destroy,
                  width=25, bg="#5a1a1a", fg="#ffffff",
                  activebackground="#7a2a2a", font=("Arial", 11), relief="flat").pack(pady=5)

        tk.Button(self.root, text="← Log Out", width=25, bg="#3c3c3c", fg="#aaaaaa",
                  activebackground="#555555", font=("Arial", 10), relief="flat",
                  command=self.show_login_screen).place(relx=0.5, rely=0.94, anchor="center")
    # * UI DESIGN of 'user Menu' screen - no logic -----finish * #
    # * Logic of 'user Menu' screen  * #

    # * Logic of 'user Menu' screen -----finish * #

    # * shared logic of all screens * #
    def clear_screen(self):
        """we use single-window design, so to navigate to new screen must clear it first"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.show_login_screen()
        self.root.mainloop()
    # * shared logic of all screens -----finish * #
