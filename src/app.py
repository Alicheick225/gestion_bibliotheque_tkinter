import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from src.views.document_view import DocumentsView
# from src.views.dashboard_view import DashboardView (à créer)

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BookWorm Haven - MVC Version")
        self.geometry("1200x800")
        
        ctk.set_appearance_mode("dark")
        
        # Conteneur principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- Chargement des Onglets ---
        
        # Onglet Livres
        self.tab_books = DocumentsView(self.notebook)
        self.notebook.add(self.tab_books, text="Livres")
        
        # Onglet Membres (A faire sur le même modèle)
        
        self.tab_members = DocumentsView(self.notebook)
        self.notebook.add(self.tab_members, text="Membres")