import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.user_controller import UserController


class MembersView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = UserController()

        # Simple table of users
        cols = ("ID", "Username", "Actif")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        tk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Deactivate", command=self.deactivate_selected).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        users = self.controller.list_users()
        for u in users:
            self.tree.insert('', tk.END, values=(u.id, u.username, u.est_actif))

    def deactivate_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez un utilisateur")
            return
        item = self.tree.item(sel[0])
        user_id = item['values'][0]
        self.controller.deactivate_user(user_id)
        self.refresh()
