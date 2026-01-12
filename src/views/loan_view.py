import tkinter as tk
from tkinter import ttk, messagebox
# import customtkinter as ctk
from src.controllers.loan_controller import LoanController


class LoanView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = LoanController()

        self.tree = ttk.Treeview(self, columns=("ID", "Membre", "Exemplaire", "Date emprunt", "Retour prévu"), show='headings')
        for c in ("ID", "Membre", "Exemplaire", "Date emprunt", "Retour prévu"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(fill=tk.X, padx=10, pady=(0,10))
        tk.Button(btns, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Retourner sélection", command=self.return_selected).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        try:
            from src.models.database import Emprunt
            emprunts = self.controller.session.query(Emprunt).all()
        except Exception:
            emprunts = []

        for e in emprunts:
            mem = e.membre.nom if getattr(e, 'membre', None) else '-'
            ex = e.exemplaire.numero_inventaire if getattr(e, 'exemplaire', None) else '-'
            self.tree.insert('', tk.END, values=(e.id, mem, ex, e.date_emprunt, e.date_retour_prevue))

    def return_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez un emprunt")
            return
        item = self.tree.item(sel[0])
        emprunt_id = item['values'][0]
        # utilisateur_retour_id: pour le moment None
        self.controller.return_exemplaire(emprunt_id, utilisateur_retour_id=None)
        self.refresh()
