from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# ==============================================================================
# 1. UTILISATEURS ET PERMISSIONS (Système & Membres)
# ==============================================================================

class TypeMembre(Base):
    __tablename__ = 'type_membre'
    
    id = Column(Integer, primary_key=True)
    libelle = Column(String(50), unique=True)
    max_emprunt = Column(Integer)            # Ex: 5 livres max
    duree_emprunt = Column(Integer)           # Ex: 14 jours
    taux_penalite_jour = Column(Float)        # Ex: 100 FCFA par jour
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    # Relation inverse
    membres = relationship("Membre", back_populates="type_membre")

class Membre(Base):
    __tablename__ = 'membre'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenoms = Column(String(150))
    adresse = Column(String(255))
    telephone = Column(String(20))
    email = Column(String(100))
    date_adhesion = Column(Date, default=datetime.now)
    est_actif = Column(Boolean, default=True)
    
    # Audit
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)
    
    # Clé étrangère
    type_membre_id = Column(Integer, ForeignKey('type_membre.id'))
    
    # Relations
    type_membre = relationship("TypeMembre", back_populates="membres")
    emprunts = relationship("Emprunt", back_populates="membre")
    reservations = relationship("Reservation", back_populates="membre")
    penalites = relationship("Penalite", back_populates="membre")

class UtilisateurSys(Base):
    """Administrateurs et Bibliothécaires"""
    __tablename__ = 'utilisateur_sys'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(255)) # Penser à hasher le mot de passe !
    est_actif = Column(Boolean, default=True)
    date_derniere_connexion = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    # Relations (pour la traçabilité)
    roles_association = relationship("UtilisateurRole", back_populates="utilisateur")
    documents_crees = relationship("Document", back_populates="createur")

class Role(Base):
    __tablename__ = 'role'
    
    id = Column(Integer, primary_key=True)
    libelle = Column(String(50)) # Ex: 'ADMIN', 'BIBLIOTHECAIRE'
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    users_association = relationship("UtilisateurRole", back_populates="role")
    permissions_association = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = 'permission'
    
    id = Column(Integer, primary_key=True)
    libelle = Column(String(100)) # Ex: 'AJOUTER_LIVRE', 'SUPPRIMER_MEMBRE'
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    roles_association = relationship("RolePermission", back_populates="permission")

# --- Tables d'association avec attributs (Classes d'association) ---

class UtilisateurRole(Base):
    __tablename__ = 'utilisateur_role'
    
    utilisateur_id = Column(Integer, ForeignKey('utilisateur_sys.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    date_creation = Column(DateTime, default=datetime.now)

    utilisateur = relationship("UtilisateurSys", back_populates="roles_association")
    role = relationship("Role", back_populates="users_association")

class RolePermission(Base):
    __tablename__ = 'role_permission'
    
    role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
    date_creation = Column(DateTime, default=datetime.now)

    role = relationship("Role", back_populates="permissions_association")
    permission = relationship("Permission", back_populates="roles_association")


# ==============================================================================
# 2. CATALOGUE ET INVENTAIRE
# ==============================================================================

# Dans src/models/database.py

class Categorie(Base):
    __tablename__ = 'categorie'
    
    id = Column(Integer, primary_key=True)
    libelle = Column(String(100))
    description = Column(Text)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)
    
    # Sous-catégories (Self-referential)
    parent_categorie_id = Column(Integer, ForeignKey('categorie.id'), nullable=True)
    
    documents = relationship("Document", back_populates="categorie")
    
    # CORRECTION ICI : On sépare la relation Parent et Enfants explicitement
    # 1. Relation pour accéder au parent (ex: sub_cat.parent)
    parent = relationship("Categorie", remote_side=[id], back_populates="enfants")
    
    # 2. Relation pour accéder aux enfants (ex: main_cat.enfants)
    enfants = relationship("Categorie", back_populates="parent")

class Editeur(Base):
    __tablename__ = 'editeur'
    
    id = Column(Integer, primary_key=True)
    libelle = Column(String(100))
    ville = Column(String(100))
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    documents = relationship("Document", back_populates="editeur")

class Auteur(Base):
    __tablename__ = 'auteur'
    
    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenoms = Column(String(150))
    nationalite = Column(String(100))
    date_naissance = Column(Date)
    date_deces = Column(Date, nullable=True)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    documents_association = relationship("DocumentAuteur", back_populates="auteur")

class Emplacement(Base):
    __tablename__ = 'emplacement'
    
    id = Column(Integer, primary_key=True)
    code_rayon = Column(String(20)) # Ex: 'RAYON-A-ETAGE-1'
    description = Column(String(255))
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)

    exemplaires = relationship("Exemplaire", back_populates="emplacement")

class Document(Base):
    """Le livre abstrait (La notice bibliographique)"""
    __tablename__ = 'document'
    
    id = Column(Integer, primary_key=True)
    titre = Column(String(255))
    annee_publication = Column(Integer)
    isbn = Column(String(20))
    resume = Column(Text)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)
    
    # Clés étrangères
    categorie_id = Column(Integer, ForeignKey('categorie.id'))
    editeur_id = Column(Integer, ForeignKey('editeur.id'))
    utilisateur_creation_id = Column(Integer, ForeignKey('utilisateur_sys.id'))
    
    # Relations
    categorie = relationship("Categorie", back_populates="documents")
    editeur = relationship("Editeur", back_populates="documents")
    createur = relationship("UtilisateurSys", back_populates="documents_crees")
    
    auteurs_association = relationship("DocumentAuteur", back_populates="document")
    exemplaires = relationship("Exemplaire", back_populates="document")
    reservations = relationship("Reservation", back_populates="document")

class DocumentAuteur(Base):
    """Lien Many-to-Many entre Document et Auteur"""
    __tablename__ = 'document_auteur'
    
    document_id = Column(Integer, ForeignKey('document.id'), primary_key=True)
    auteur_id = Column(Integer, ForeignKey('auteur.id'), primary_key=True)
    date_creation = Column(DateTime, default=datetime.now)

    document = relationship("Document", back_populates="auteurs_association")
    auteur = relationship("Auteur", back_populates="documents_association")

class Exemplaire(Base):
    """Le livre physique (avec code barre/numéro inventaire)"""
    __tablename__ = 'exemplaire'
    
    id = Column(Integer, primary_key=True)
    numero_inventaire = Column(String(50), unique=True)
    etat = Column(String(50)) # Ex: 'Neuf', 'Bon', 'Abimé'
    statut = Column(String(50)) # Ex: 'Disponible', 'Emprunté', 'Perdu'
    date_mise_en_service = Column(Date)
    date_creation = Column(DateTime, default=datetime.now)
    date_modification = Column(DateTime, onupdate=datetime.now)
    
    emplacement_id = Column(Integer, ForeignKey('emplacement.id'))
    document_id = Column(Integer, ForeignKey('document.id'))
    utilisateur_ajout_id = Column(Integer, ForeignKey('utilisateur_sys.id')) # Trace qui a ajouté la copie physique

    emplacement = relationship("Emplacement", back_populates="exemplaires")
    document = relationship("Document", back_populates="exemplaires")
    emprunts = relationship("Emprunt", back_populates="exemplaire")


# ==============================================================================
# 3. ENTITES TRANSACTIONNELLES (Emprunts, Réservations, Amendes)
# ==============================================================================

class Emprunt(Base):
    __tablename__ = 'emprunt'
    
    id = Column(Integer, primary_key=True)
    date_emprunt = Column(DateTime, default=datetime.now)
    date_retour_prevue = Column(Date)
    date_retour_reelle = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, default=datetime.now)
    
    membre_id = Column(Integer, ForeignKey('membre.id'))
    exemplaire_id = Column(Integer, ForeignKey('exemplaire.id'))
    
    # Qui a validé le prêt et le retour ?
    utilisateur_emprunt_id = Column(Integer, ForeignKey('utilisateur_sys.id'))
    utilisateur_retour_id = Column(Integer, ForeignKey('utilisateur_sys.id'), nullable=True)

    membre = relationship("Membre", back_populates="emprunts")
    exemplaire = relationship("Exemplaire", back_populates="emprunts")
    penalites = relationship("Penalite", back_populates="emprunt")

class Reservation(Base):
    __tablename__ = 'reservation'
    
    id = Column(Integer, primary_key=True)
    date_reservation = Column(DateTime, default=datetime.now)
    date_disponibilite = Column(DateTime, nullable=True) # Quand le livre revient
    statut = Column(String(50)) # 'En attente', 'Validée', 'Annulée'
    date_expiration_mise_de_cote = Column(DateTime, nullable=True)
    date_modification_statut = Column(DateTime, onupdate=datetime.now)
    
    membre_id = Column(Integer, ForeignKey('membre.id'))
    document_id = Column(Integer, ForeignKey('document.id')) # On réserve un Titre, pas un exemplaire précis

    membre = relationship("Membre", back_populates="reservations")
    document = relationship("Document", back_populates="reservations")

class Penalite(Base):
    __tablename__ = 'penalite'
    
    id = Column(Integer, primary_key=True)
    montant_du = Column(Float)
    montant_paye = Column(Float, default=0.0)
    motif = Column(String(255)) # Ex: 'Retard', 'Livre abimé'
    statut = Column(String(50)) # 'Non payé', 'Partiellement payé', 'Soldé'
    date_creation = Column(DateTime, default=datetime.now)
    date_modification_statut = Column(DateTime, onupdate=datetime.now)
    
    membre_id = Column(Integer, ForeignKey('membre.id'))
    emprunt_id = Column(Integer, ForeignKey('emprunt.id'), nullable=True)
    utilisateur_creation_id = Column(Integer, ForeignKey('utilisateur_sys.id'))

    membre = relationship("Membre", back_populates="penalites")
    emprunt = relationship("Emprunt", back_populates="penalites")

# Initialisation de la DB
engine = create_engine('sqlite:///bibliotheque.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)