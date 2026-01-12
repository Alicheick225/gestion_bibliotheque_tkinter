import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.document_controller import DocumentController

class DocumentsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = DocumentController() # On connecte le cerveau

        # --- Barre de recherche ---
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.entry_search = tk.Entry(search_frame)
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_search = tk.Button(search_frame, text="Search", width=10, command=self.perform_search)
        btn_search.pack(side=tk.LEFT)
        
        self.btn_add = tk.Button(search_frame, text="Add Book", width=10, command=self.show_add_dialog)
        self.btn_add.pack(side=tk.RIGHT)

        # --- Tableau (Treeview) ---
        columns = ("ID", "Titre", "Année", "ISBN", "Catégorie", "Disponibles")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bouton Refresh
        tk.Button(self, text="Refresh List", command=self.refresh_table).pack(pady=5)
        
        # Charger les données au démarrage
        self.refresh_table()

    def refresh_table(self):
        # 1. Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 2. Demander les données au Contrôleur
        documents = self.controller.get_all_documents()
        
        # 3. Remplir le tableau
        for d in documents:
            # catégorie
            cat = d.categorie.libelle if d.categorie else "-"
            # nombre d'exemplaires disponibles
            disponibles = 0
            try:
                for ex in d.exemplaires:
                    if getattr(ex, 'statut', '').lower() == 'disponible':
                        disponibles += 1
            except Exception:
                disponibles = 0

            self.tree.insert("", tk.END, values=(d.id, d.titre, d.annee_publication, d.isbn, cat, disponibles))

    def perform_search(self):
        query = self.entry_search.get()
        documents = self.controller.search_documents(query)
        # Mettre à jour le tableau avec la liste filtrée
        for item in self.tree.get_children():
            self.tree.delete(item)
        for d in documents:
            cat = d.categorie.libelle if d.categorie else "-"
            disponibles = sum(1 for ex in d.exemplaires if getattr(ex, 'statut', '').lower() == 'disponible')
            self.tree.insert("", tk.END, values=(d.id, d.titre, d.annee_publication, d.isbn, cat, disponibles))

    def set_current_user(self, user, roles: list):
        """Adjust UI depending on the authenticated user's roles.
        - Members: cannot add books
        - Bibliothécaire / Admin: can add books
        """
        self.current_user = user
        self.current_roles = roles or []
        allowed = any(r.upper() in ("ADMIN", "BIBLIOTHECAIRE") for r in self.current_roles)
        try:
            if allowed:
                self.btn_add.configure(state="normal")
            else:
                self.btn_add.configure(state="disabled")
        except Exception:
            pass

    def show_add_dialog(self):
        # Ici tu mets ton code de Toplevel (dialogue)
        # Mais au moment de sauvegarder, tu fais :
        # self.controller.add_book(title, author, ...)
        # self.refresh_table()
        
        pass