import tkinter as tk
from tkinter import ttk, messagebox
# import customtkinter as ctk
from src.controllers.penalty_controller import PenaltyController


class PenaltyView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = PenaltyController()

        self.tree = ttk.Treeview(self, columns=("ID", "Membre", "Montant dû", "Payé", "Statut"), show='headings')
        for c in ("ID", "Membre", "Montant dû", "Payé", "Statut"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(fill=tk.X, padx=10, pady=(0,10))
        tk.Button(btns, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        try:
            from src.models.database import Penalite
            penalites = self.controller.session.query(Penalite).all()
        except Exception:
            penalites = []

        for p in penalites:
            mem = p.membre.nom if getattr(p, 'membre', None) else '-'
            self.tree.insert('', tk.END, values=(p.id, mem, p.montant_du, p.montant_paye, p.statut))
