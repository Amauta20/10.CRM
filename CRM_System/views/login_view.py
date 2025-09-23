import tkinter as tk
from tkinter import ttk, messagebox
from CRM_System.controllers.auth_controller import AuthController

class LoginWindow(tk.Tk):
    def __init__(self, i18n, on_success):
        super().__init__()
        self.i18n = i18n
        self.on_success = on_success
        self.auth_controller = AuthController()

        self.title(self.i18n.get("login_window", "title"))
        self.geometry("350x200")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(self.frame, text=self.i18n.get("login_window", "username_label")).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        # Password
        ttk.Label(self.frame, text=self.i18n.get("login_window", "password_label")).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.login_button = ttk.Button(button_frame, text=self.i18n.get("login_window", "login_button"), command=self.handle_login)
        self.login_button.pack(side=tk.LEFT, padx=5)

        self.register_button = ttk.Button(button_frame, text=self.i18n.get("login_window", "register_button"), command=self.handle_register)
        self.register_button.pack(side=tk.LEFT, padx=5)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("login_window", "empty_fields_error"))
            return

        user = self.auth_controller.authenticate_user(username, password)

        if user:
            self.destroy()  # Close login window
            self.on_success(user) # Open main app
        else:
            messagebox.showerror(self.i18n.get("messagebox", "error"), self.i18n.get("login_window", "invalid_credentials_error"))

    def handle_register(self):
        # For simplicity, using simple dialogs. A custom Toplevel would be better for a real app.
        username = tk.simpledialog.askstring(self.i18n.get("register_window", "title"), self.i18n.get("register_window", "username_prompt"), parent=self)
        if not username:
            return

        full_name = tk.simpledialog.askstring(self.i18n.get("register_window", "title"), self.i18n.get("register_window", "fullname_prompt"), parent=self)
        if not full_name:
            return

        password = tk.simpledialog.askstring(self.i18n.get("register_window", "title"), self.i18n.get("register_window", "password_prompt"), show='*', parent=self)
        if not password:
            return

        try:
            self.auth_controller.create_user(username, password, full_name)
            messagebox.showinfo(self.i18n.get("messagebox", "success"), self.i18n.get("register_window", "success_message"))
        except ValueError as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), str(e))
        except Exception as e:
            messagebox.showerror(self.i18n.get("messagebox", "error"), f"{self.i18n.get("register_window", "generic_error")} {e}")
