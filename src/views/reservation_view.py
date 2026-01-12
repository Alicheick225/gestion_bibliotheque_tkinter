import tkinter as tk
from tkinter import ttk, messagebox
# import customtkinter as ctk
from src.controllers.reservation_controller import ReservationController


class ReservationView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ReservationController()

        # Simple UI: list + create
        self.tree = ttk.Treeview(self, columns=("ID", "Document", "Membre", "Statut"), show='headings')
        for c in ("ID", "Document", "Membre", "Statut"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack(fill=tk.X, padx=10, pady=(0,10))
        tk.Button(btns, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Annuler sélection", command=self.cancel_selected).pack(side=tk.LEFT, padx=5)

        self.refresh()

    def refresh(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        try:
            from src.models.database import Reservation
            res = self.controller.session.query(Reservation).all()
        except Exception:
            res = []

        for r in res:
            doc = r.document.titre if getattr(r, 'document', None) else '-'
            mem = r.membre.nom if getattr(r, 'membre', None) else '-'
            self.tree.insert('', tk.END, values=(r.id, doc, mem, r.statut))

    def cancel_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Sélectionnez une réservation")
            return
        item = self.tree.item(sel[0])
        res_id = item['values'][0]
        self.controller.cancel_reservation(res_id)
        self.refresh()
