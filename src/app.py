import tkinter as tk
from tkinter import ttk
# import customtkinter as ctk
from src.views.document_view import DocumentsView
from src.views.login_view import LoginView
from src.views.members_view import MembersView
from src.views.reservation_view import ReservationView
from src.views.loan_view import LoanView
from src.views.penalty_view import PenaltyView

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BookWorm Haven - MVC Version")
        self.geometry("1200x800")
        
        # ctk.set_appearance_mode("dark")
        
        # Conteneur principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Menu pour la déconnexion
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        self.user_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Utilisateur", menu=self.user_menu)
        self.user_menu.add_command(label="Déconnexion", command=self._logout, state="disabled")
        
        # Préparer les vues (sans les ajouter encore)
        self.tab_books = DocumentsView(self.notebook)
        self.tab_reservations = ReservationView(self.notebook)
        self.tab_loans = LoanView(self.notebook)
        self.tab_penalties = PenaltyView(self.notebook)
        self.tab_members = MembersView(self.notebook)
        
        # Onglet Connexion seulement au départ
        self.tab_login = LoginView(self.notebook, on_login=self._on_login)
        self.notebook.add(self.tab_login, text="Connexion")

    def _on_login(self, user, roles: list):
        # stocker l'utilisateur courant
        self.current_user = user
        self.current_roles = roles or []
        
        print(f"DEBUG: Utilisateur {user.username} connecté avec rôles: {self.current_roles}")
        
        # Masquer l'onglet Connexion
        try:
            self.notebook.forget(self.tab_login)
        except Exception:
            pass
        
        # Ajouter les onglets selon le rôle
        is_admin = any(r.upper() == 'ADMIN' for r in self.current_roles)
        is_bibliothecaire = any(r.upper() == 'BIBLIOTHECAIRE' for r in self.current_roles)
        is_membre = any(r.upper() == 'MEMBRE' for r in self.current_roles) or not self.current_roles  # par défaut membre
        
        print(f"DEBUG: is_admin={is_admin}, is_bibliothecaire={is_bibliothecaire}, is_membre={is_membre}")
        
        # Toujours ajouter Livres
        self.notebook.add(self.tab_books, text="Livres")
        
        # Pour tous : Réservations et Emprunts
        self.notebook.add(self.tab_reservations, text="Réservations")
        self.notebook.add(self.tab_loans, text="Emprunts")
        
        # Pour bibliothécaire et admin : Pénalités
        if is_bibliothecaire or is_admin:
            self.notebook.add(self.tab_penalties, text="Pénalités")
        
        # Pour admin : Membres
        if is_admin:
            print("DEBUG: Ajout de l'onglet Membres")
            self.notebook.add(self.tab_members, text="Membres")
        
        # Propager l'utilisateur aux vues
        try:
            if hasattr(self.tab_books, 'set_current_user'):
                self.tab_books.set_current_user(user, roles)
        except Exception:
            pass
        
        # Basculer sur l'onglet Livres
        try:
            self.notebook.select(self.tab_books)
        except Exception:
            pass
        
        # Activer le menu de déconnexion
        self.user_menu.entryconfig("Déconnexion", state="normal")

    def _logout(self):
        # Masquer tous les onglets sauf Connexion
        try:
            self.notebook.forget(self.tab_books)
        except Exception:
            pass
        try:
            self.notebook.forget(self.tab_reservations)
        except Exception:
            pass
        try:
            self.notebook.forget(self.tab_loans)
        except Exception:
            pass
        try:
            self.notebook.forget(self.tab_penalties)
        except Exception:
            pass
        try:
            self.notebook.forget(self.tab_members)
        except Exception:
            pass
        
        # Réafficher l'onglet Connexion
        try:
            self.notebook.add(self.tab_login, text="Connexion")
            self.notebook.select(self.tab_login)
        except Exception:
            pass
        
        # Désactiver le menu de déconnexion
        self.user_menu.entryconfig("Déconnexion", state="disabled")
        
        # Réinitialiser l'utilisateur courant
        self.current_user = None
        self.current_roles = []