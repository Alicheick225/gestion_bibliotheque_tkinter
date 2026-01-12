import tkinter as tk
from tkinter import messagebox
from src.controllers.auth_controller import AuthController


class LoginView(tk.Frame):
    def __init__(self, parent, on_login=None):
        super().__init__(parent)
        self.controller = AuthController()
        self.on_login = on_login

        self.columnconfigure(0, weight=1)

        self.label = tk.Label(self, text="Connexion")
        self.label.grid(row=0, column=0, pady=(10, 5))

        self.entry_username = tk.Entry(self)
        self.entry_username.grid(row=1, column=0, padx=20, pady=5, sticky='ew')

        self.entry_password = tk.Entry(self, show='*')
        self.entry_password.grid(row=2, column=0, padx=20, pady=5, sticky='ew')

        self.btn_login = tk.Button(self, text="Se connecter", command=self.do_login)
        self.btn_login.grid(row=3, column=0, padx=20, pady=10)

    def do_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user = self.controller.authenticate(username, password)
        if user:
            roles = self.controller.get_roles(user)
            messagebox.showinfo("Succès", f"Bienvenu {user.username}")
            if callable(self.on_login):
                self.on_login(user, roles)
        else:
            messagebox.showerror("Erreur", "Identifiants invalides")
