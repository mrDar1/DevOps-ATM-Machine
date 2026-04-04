import tkinter as tk
from tkinter import ttk, messagebox
from storage import load_data, save_data


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
                self.current_account_id = account_id
                self.current_pin = pin
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
        self.balance_label = tk.Label(info_frame, text=f"Balance: ${account.balance:,.2f}", bg="#2e2e2e", fg="#4caf50",
                                      font=("Arial", 13, "bold"))
        self.balance_label.pack(pady=(4, 12))

        # --- buttons frame ---
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.place(relx=0.5, rely=0.57, anchor="center")

        btn_cfg = dict(width=25, bg="#3c3c3c", fg="#ffffff",
                       activebackground="#555555", font=("Arial", 11), relief="flat")

        deposit_btn = tk.Button(btn_frame, text="Deposit", **btn_cfg)
        deposit_btn.pack(pady=5)
        deposit_btn.config(command=self.handle_deposit)
        withdraw_btn = tk.Button(btn_frame, text="Withdraw",   **btn_cfg)
        withdraw_btn.pack(pady=5)
        withdraw_btn.config(command=self.handle_withdraw)
        transfer_btn = tk.Button(btn_frame, text="Transfer",       **btn_cfg)
        transfer_btn.pack(pady=5)
        transfer_btn.config(command=self.handle_transfer)
        history_btn = tk.Button(btn_frame, text="History",    **btn_cfg)
        history_btn.pack(pady=5)
        history_btn.config(command=self.handle_history)
        change_pin_btn = tk.Button(btn_frame, text="Change PIN", **btn_cfg)
        change_pin_btn.pack(pady=5)
        change_pin_btn.config(command=self.handle_change_pin)
        exit_btn = tk.Button(btn_frame, text="Exit entire App", **btn_cfg)
        exit_btn.pack(pady=5)
        exit_btn.config(command=self.handle_exit)

        tk.Button(self.root, text="← Log Out", width=25, bg="#3c3c3c", fg="#aaaaaa",
                  activebackground="#555555", font=("Arial", 10), relief="flat",
                  command=self.show_login_screen).place(relx=0.5, rely=0.94, anchor="center")
    # * UI DESIGN of 'user Menu' screen - no logic -----finish * #

    # * Logic of 'user Menu' screen  * #
    def handle_deposit(self):
        window = tk.Toplevel(self.root)
        window.title("הפקדה")

        tk.Label(window, text="Enter amount:").pack(pady=10)
        amount_entry = tk.Entry(window)
        amount_entry.pack(pady=5)

        def confirm_deposit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be a positive number", parent=window)
                    return
            except ValueError:
                messagebox.showerror("Error", "Amount must be a positive number", parent=window)
                return

            account = self.bank.get_account(self.current_account_id)
            success = account.deposit(amount, self.current_pin)
            if success:
                save_data(self.bank)
                self.balance_label.config(text=f"Balance: ${account.balance:,.2f}")
                messagebox.showinfo("Success", f"Deposited ${amount:,.2f} successfully", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", "Deposit failed", parent=window)

        tk.Button(window, text="Deposit", command=confirm_deposit).pack(pady=10)

    def handle_withdraw(self):
        window = tk.Toplevel(self.root)
        window.title("משיכה")

        tk.Label(window, text="Enter amount:").pack(pady=10)
        amount_entry = tk.Entry(window)
        amount_entry.pack(pady=5)

        def confirm_withdraw():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be a positive number", parent=window)
                    return
            except ValueError:
                messagebox.showerror("Error", "Amount must be a positive number", parent=window)
                return

            account = self.bank.get_account(self.current_account_id)
            success = account.withdraw(amount, self.current_pin)
            if success:
                save_data(self.bank)
                self.balance_label.config(text=f"Balance: ${account.balance:,.2f}")
                messagebox.showinfo("Success", f"Withdrew ${amount:,.2f} successfully", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", "Withdrawal failed", parent=window)

        tk.Button(window, text="Withdraw", command=confirm_withdraw).pack(pady=10)

    def handle_transfer(self):
        window = tk.Toplevel(self.root)
        window.title("Transfer")
        window.geometry("280x200")

        tk.Label(window, text="Destination ID:").pack(pady=(14, 2))
        dest_entry = tk.Entry(window)
        dest_entry.pack(pady=2)

        tk.Label(window, text="Amount:").pack(pady=(10, 2))
        amount_entry = tk.Entry(window)
        amount_entry.pack(pady=2)

        def confirm_transfer():
            # validate destination ID input
            try:
                dest_id = int(dest_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Destination ID must be a number", parent=window)
                return

            # validate amount input
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Amount must be a positive number", parent=window)
                return

            # same account check
            if dest_id == self.current_account_id:
                messagebox.showerror("Error", "Cannot transfer to your own account", parent=window)
                return

            # destination exists check
            dest_account = self.bank.get_account(dest_id)
            if dest_account is None:
                messagebox.showerror("Error", f"Account {dest_id} does not exist", parent=window)
                return

            # destination blocked check
            if dest_account.is_blocked:
                messagebox.showerror("Error", "Destination account is blocked", parent=window)
                return

            # sufficient balance check
            sender = self.bank.get_account(self.current_account_id)
            if amount > sender.balance:
                messagebox.showerror("Error", "Insufficient balance", parent=window)
                return

            success, message = self.bank.transaction_to_from_accounts(
                self.current_account_id, dest_id, amount, self.current_pin
            )
            if success:
                save_data(self.bank)
                self.balance_label.config(text=f"Balance: ${sender.balance:,.2f}")
                messagebox.showinfo("Success", f"Transferred ${amount:,.2f} to account {dest_id}", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", message, parent=window)

        tk.Button(window, text="Transfer", command=confirm_transfer).pack(pady=14)

    def handle_history(self):
        """use fitussi first easier option: 'insert(tk.End, text) and not
        'tk.Text' and "STATE=DISABLED" to make it read-only, because easier and only 'read'"""
        account = self.bank.get_account(self.current_account_id)
        window = tk.Toplevel(self.root)
        window.title("Transaction History")
        window.geometry("420x300")

        tk.Label(window, text="Transaction History", font=("Arial", 14, "bold")).pack(pady=8)

        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Courier", 10), width=55)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        if not account.actions_log:
            listbox.insert(tk.END, "  No transactions yet.")
        else:
            for action in account.actions_log:
                time_str = action["time"].strftime("%Y-%m-%d %H:%M")
                amount_str = f"${action['amount']:,.2f}"
                action_type = action["type"].replace("_", " ").title()
                counterparty = f" -> {action['counterparty']}" if action["counterparty"] else ""
                listbox.insert(tk.END, f"  {time_str}  {action_type:<18} {amount_str}{counterparty}")

        tk.Button(window, text="Close", command=window.destroy).pack(pady=8)

    def handle_change_pin(self):
        window = tk.Toplevel(self.root)
        window.title("Change PIN")
        window.geometry("280x220")
        window.configure(bg="#1e1e1e")

        lbl_cfg = dict(bg="#1e1e1e", fg="#aaaaaa", font=("Arial", 10))
        entry_cfg = dict(width=22, show="*", bg="#2e2e2e", fg="#ffffff",
                         insertbackground="#ffffff", relief="flat", font=("Arial", 12))

        tk.Label(window, text="Current PIN", **lbl_cfg).pack(pady=(18, 2))
        current_entry = tk.Entry(window, **entry_cfg)
        current_entry.pack()

        tk.Label(window, text="New PIN", **lbl_cfg).pack(pady=(10, 2))
        new_entry = tk.Entry(window, **entry_cfg)
        new_entry.pack()

        tk.Label(window, text="Verify New PIN", **lbl_cfg).pack(pady=(10, 2))
        verify_entry = tk.Entry(window, **entry_cfg)
        verify_entry.pack()

        def confirm_change():
            try:
                old_pin = int(current_entry.get())
                new_pin = int(new_entry.get())
                verify_pin = int(verify_entry.get())
            except ValueError:
                messagebox.showerror("Error", "PIN must be a number", parent=window)
                return

            if new_pin != verify_pin:
                messagebox.showerror("Error", "New PINs do not match", parent=window)
                return

            account = self.bank.get_account(self.current_account_id)
            if account.change_pin(old_pin, new_pin):
                self.current_pin = new_pin
                save_data(self.bank)
                messagebox.showinfo("Success", "PIN changed successfully", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", "Current PIN is incorrect", parent=window)

        tk.Button(window, text="Change PIN", bg="#3c3c3c", fg="#ffffff",
                  activebackground="#555555", relief="flat",
                  command=confirm_change).pack(pady=14)

    def handle_exit(self):
        self.root.destroy()
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
