# import ctypes
import tkinter as tk
from tkinter import ttk
from models import Bank, Account
import styles
import datetime as dt
# Fix pixelation on Windows
# try:
#     ctypes.windll.shcore.SetProcessDpiAwareness(1)
# except Exception:
#     try:
#         ctypes.windll.user32.SetProcessDPIAware()
#     except Exception:
#         pass

class ATMApp(tk.Tk):
    def __init__(self, bank: Bank):
        super().__init__()
        self.bank = bank
        self.account: Account
        self.title("DevOps ATM")
        # self.geometry(f"{styles.window_width}x{styles.window_hight}")
        self.resizable(False, False)
        self.configure(bg=styles.color_dark_bg)
        
        # holds pages on top of each other
        container = tk.Frame(self, bg=styles.color_dark_bg)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        
        frame = LoginPage(parent=container, controller=self)
        self.frames[LoginPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(LoginPage)
        
        
    def show_frame(self, page_class: tk.Frame):
        frame = self.frames[page_class]
        frame.tkraise()
    

class LogPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.bank: Bank = controller.bank
        self.account: Account = controller.account
        # self.account: Account = controller.account
        super().__init__(parent, style="Log.TFrame")
        self.controller = controller


        # Configure Styles for this page
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.page_titles()

        self.actions_log: list[dict[dt.datetime, float, str, str]] = self.account.actions_log

        for action in self.actions_log:
            new_card: tk.Frame = self.log_card(amount=action["amount"],datetime=action["time"],action_type=action["type"],counter_party=action["counterparty"])
            new_card.pack(pady=5, padx=62, fill="x")

    def page_titles(self):
         # Frame styles
        
        self.style.configure("Log.TFrame", background=styles.color_dark_bg)
        # Label styles
        self.style.configure("LogTitle.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_terminal_green,
                             font=styles.font_page_title)
        
        self.style.configure("LogIcon.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_terminal_yellow,
                             font=styles.font_page_title)
        
        self.style.configure("LogSubtitle.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_text_color,
                             font=styles.font_page_sub_title)
        
        #---titles---
        self.title_frame = ttk.Frame(self, style="Log.TFrame")
        self.title_frame.pack(pady=(102, 0), padx=62, fill="x")
        
        self.page_title = ttk.Label(
            self.title_frame, 
            text=".LOG", 
            style="LogTitle.TLabel"
        )
        self.page_title.pack(side="left")
        
        self.log_icon_image = tk.PhotoImage(file="images/archive icon.png")

        self.page_icon = tk.Label(
            self.title_frame,
            background=styles.color_dark_bg,
            image=self.log_icon_image,
            borderwidth=0,
            highlightthickness=0
        )
        self.page_icon.pack(side="top",anchor="ne")
        
        self.page_subtitle = ttk.Label(
            self, 
            text="Past_Activities", 
            style="LogSubtitle.TLabel"
        )
        self.page_subtitle.pack(pady=(0, 20), padx=62, anchor="w")

    def log_card(self, amount: float, datetime: dt.datetime, action_type: str, counter_party: str) -> tk.Frame: #counter_party
        frame_outside = tk.Frame(self,background=styles.color_less_dark_bg, height=2)
        frame_inside = tk.Frame(frame_outside, background=styles.color_dark_bg)
        amount_lable = tk.Label(frame_inside, text=("₪"+str(amount)),font=styles.font_button, foreground=styles.color_text_color,background=styles.color_dark_bg)
        datetime_label = tk.Label(frame_inside, text=datetime.strftime("%d/%m/%y %H:%M"), background=styles.color_dark_bg, font=styles.font_detils, foreground=styles.color_text_color)
        if action_type == "withdraw":
            action_type_label = tk.Label(frame_inside, text="WITHDRAW",font=styles.font_field, background=styles.color_dark_bg, foreground=styles.color_terminal_red)
            action_counterparty_label = tk.Label(frame_inside, text=counter_party,font=styles.font_detils, background=styles.color_dark_bg, foreground=styles.color_text_color)
        elif action_type == "deposit":
            action_type_label = tk.Label(frame_inside, text="DEPOSIT",font=styles.font_field, background=styles.color_dark_bg, foreground=styles.color_terminal_green)
            action_counterparty_label = tk.Label(frame_inside, text=counter_party,font=styles.font_detils, background=styles.color_dark_bg, foreground=styles.color_text_color)
        elif action_type == "transaction_in":
            action_type_label = tk.Label(frame_inside, text="FROM",font=styles.font_field, background=styles.color_dark_bg, foreground=styles.color_terminal_green)
            action_counterparty_label = tk.Label(frame_inside, text=counter_party,font=styles.font_detils, background=styles.color_dark_bg, foreground=styles.color_text_color)
        elif action_type == "transaction_out":
            action_type_label = tk.Label(frame_inside, text="TO",font=styles.font_field, background=styles.color_dark_bg, foreground=styles.color_terminal_red)
            action_counterparty_label = tk.Label(frame_inside, text=counter_party,font=styles.font_detils, background=styles.color_dark_bg, foreground=styles.color_text_color)
        else:
            action_type_label = tk.Label(frame_inside, text="Error",font=styles.font_field, background=styles.color_dark_bg, foreground=styles.color_terminal_yellow)

        frame_inside.pack(side="top", fill="x", pady=(0, 2))
        frame_inside.grid_columnconfigure(0, weight=1)

        amount_lable.grid(row=0, sticky="nw")
        action_type_label.grid(row=0, sticky="ne")
        datetime_label.grid(row=1, sticky="sw")
        action_counterparty_label.grid(row=1, sticky="se")


        return frame_outside


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.bank: Bank = controller.bank

        # Configure Styles for this page
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame styles
        self.style.configure("Login.TFrame", background=styles.color_dark_bg)
        self.style.configure("Input.TFrame", background=styles.color_less_dark_bg)
        
        # Label styles
        self.style.configure("LoginTitle.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_terminal_green,
                             font=styles.font_page_title)
        
        self.style.configure("LoginIcon.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_terminal_yellow,
                             font=styles.font_page_title)
        
        self.style.configure("LoginSubtitle.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_text_color,
                             font=styles.font_page_sub_title)
        
        self.style.configure("LoginDetail.TLabel", 
                             background=styles.color_dark_bg, 
                             foreground=styles.color_terminal_green,
                             font=styles.font_detils)
        
        # Entry style
        # self.style.configure("Login.TEntry", 
        #                      fieldbackground=styles.color_less_dark_bg,
        #                      foreground=styles.color_text_color,
        #                      insertbackground=styles.color_text_color,
        #                      relief="flat",
        #                      borderwidth=0,
        #                      highlightthickness=0,
        #                      bordercolor=styles.color_less_dark_bg
        #                      )
        
        # Button style
        self.style.configure("Login.TButton",
                             background=styles.color_terminal_green,
                             foreground=styles.color_dark_bg,
                             font=styles.font_button,
                             padding=(20,24),
                             anchor="w",
                             borderwidth=0, relief="flat")
        self.style.map("Login.TButton",
                       background=[('active', styles.color_terminal_green), ('pressed', styles.color_terminal_green)])

        super().__init__(parent, style="Login.TFrame")
        self.controller = controller
        self.parent = parent
        
        #---titles---
        self.title_frame = ttk.Frame(self, style="Login.TFrame")
        self.title_frame.pack(pady=(102, 0), padx=62, fill="x")
        
        self.page_title = ttk.Label(
            self.title_frame, 
            text="DevOps", 
            style="LoginTitle.TLabel"
        )
        self.page_title.pack(side="left")
        
        self.page_icon = ttk.Label(
            self.title_frame, 
            text="V1.0.3", 
            style="LoginIcon.TLabel"
        )
        self.page_icon.pack(side="right")
        
        self.page_subtitle = ttk.Label(
            self, 
            text="ATM_MACHINE", 
            style="LoginSubtitle.TLabel"
        )
        self.page_subtitle.pack(pady=(0, 20), padx=62, anchor="w")
                
        #---id---
        self.id_label = ttk.Label(
            self,
            text="> SSH_TO_YOUR_MACHINE_",
            style="LoginDetail.TLabel"
        )
        self.id_label.pack(padx=62, anchor="w")

        self.id_entry_frame_line = tk.Frame(
            self,
            bg=styles.color_terminal_green,
            height=2
        )
        self.id_entry_frame_line.pack(pady=(5, 12), padx=62, fill='x', anchor="w")
        
        self.id_entry_frame_background = ttk.Frame(
            self.id_entry_frame_line,
            style="Input.TFrame"
        )
        self.id_entry_frame_background.pack(side="top", fill="x", pady=(0, 2))
        
        self.id_entry = tk.Entry(
            self.id_entry_frame_background,
            font=styles.font_field,
            background=styles.color_less_dark_bg,
            foreground=styles.color_text_color,
            borderwidth=0,
            highlightthickness=0,
            insertbackground=styles.color_text_color
  
        )
        self.id_entry.pack(side="top", fill="x", ipady=12, padx=15)
        
        #---pin---
        self.pin_label = ttk.Label(
            self,
            text="> ENTER_PIN_",
            style="LoginDetail.TLabel"
        )
        self.pin_label.pack(padx=62, anchor="w")

        self.pin_entry_frame_line = tk.Frame(
            self,
            bg=styles.color_terminal_green,
            height=2
        )
        self.pin_entry_frame_line.pack(pady=(5, 12), padx=62, fill='x', anchor="w")
        
        self.pin_entry_frame_background = ttk.Frame(
            self.pin_entry_frame_line,
            style="Input.TFrame"
        )
        self.pin_entry_frame_background.pack(side="top", fill="x", pady=(0, 2))
        
        self.pin_entry = tk.Entry(
            self.pin_entry_frame_background,
            font=styles.font_field,
            background=styles.color_less_dark_bg,
            foreground=styles.color_text_color,
            borderwidth=0,
            highlightthickness=0,
            insertbackground=styles.color_text_color,
            show="*"  
        )
        self.pin_entry.pack(side="top", fill="x", ipady=12, padx=15)
        
        self.auth_button = ttk.Button(
            self,
            text="SHH_AUTHENTICATE",
            style="Login.TButton",
            cursor="hand2",
            command=self.login_button_acion
        )
        self.auth_button.pack(pady=(20, 102), padx=62, fill="x", anchor="w")
    
    def login_button_acion(self):
        input_id: str = self.id_entry.get()
        input_pin: str = self.pin_entry.get()
        if input_id.isdigit() and input_pin.isdigit():
            login: tuple = self.bank.log_in_account(account_id=int(input_id),pin=int(input_pin))
            if login[0]:
                print(login[1])

                self.controller.account: Account = self.bank.get_account(int(input_id))

                frame = LogPage(parent=self.parent, controller=self.controller)
                self.controller.frames[LogPage] = frame
                frame.grid(row=0, column=0, sticky="nsew")

                self.controller.show_frame(LogPage)
            else:
                print(login[1])   
        else:
            print("invalid input")
            

