import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.controllers.document_controller import DocumentController

class DocumentsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = DocumentController() # On connecte le cerveau

        # --- Barre de recherche ---
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Search books...")
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_search = ctk.CTkButton(search_frame, text="Search", width=100, command=self.perform_search)
        btn_search.pack(side=tk.LEFT)
        
        btn_add = ctk.CTkButton(search_frame, text="Add Book", width=100, command=self.show_add_dialog)
        btn_add.pack(side=tk.RIGHT)

        # --- Tableau (Treeview) ---
        columns = ("ID", "Title", "Author", "ISBN", "Genre", "Available")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Bouton Refresh
        ctk.CTkButton(self, text="Refresh List", command=self.refresh_table).pack(pady=5)
        
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
            status = "Yes" if d.available else "No"
            self.tree.insert("", tk.END, values=(d.id, d.title, d.author, d.isbn, d.genre, status))

    def perform_search(self):
        query = self.entry_search.get()
        documents = self.controller.search_documents(query)
        # ... (code pour mettre à jour le tableau, identique à refresh_table mais avec la liste filtrée)

    def show_add_dialog(self):
        # Ici tu mets ton code de Toplevel (dialogue)
        # Mais au moment de sauvegarder, tu fais :
        # self.controller.add_book(title, author, ...)
        # self.refresh_table()
        pass