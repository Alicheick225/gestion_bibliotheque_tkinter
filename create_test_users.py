#!/usr/bin/env python3
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.environ['MACOSX_DEPLOYMENT_TARGET'] = '10.14'

from src.models.database import Session, UtilisateurSys, Role, UtilisateurRole
from src.controllers.auth_controller import AuthController

def create_test_users():
    session = Session()
    
    # Créer les rôles s'ils n'existent pas
    admin_role = session.query(Role).filter_by(libelle='ADMIN').first()
    if not admin_role:
        admin_role = Role(libelle='ADMIN')
        session.add(admin_role)
    
    biblio_role = session.query(Role).filter_by(libelle='BIBLIOTHECAIRE').first()
    if not biblio_role:
        biblio_role = Role(libelle='BIBLIOTHECAIRE')
        session.add(biblio_role)
    
    membre_role = session.query(Role).filter_by(libelle='MEMBRE').first()
    if not membre_role:
        membre_role = Role(libelle='MEMBRE')
        session.add(membre_role)
    
    session.commit()
    
    # Créer les utilisateurs de test
    auth = AuthController()
    
    # Admin
    admin = auth.create_user('admin', 'admin123')
    admin_role_assoc = UtilisateurRole(utilisateur_id=admin.id, role_id=admin_role.id)
    session.add(admin_role_assoc)
    
    # Bibliothécaire
    biblio = auth.create_user('biblio', 'biblio123')
    biblio_role_assoc = UtilisateurRole(utilisateur_id=biblio.id, role_id=biblio_role.id)
    session.add(biblio_role_assoc)
    
    # Membre
    membre = auth.create_user('membre', 'membre123')
    membre_role_assoc = UtilisateurRole(utilisateur_id=membre.id, role_id=membre_role.id)
    session.add(membre_role_assoc)
    
    session.commit()
    session.close()
    
    print("Utilisateurs de test créés :")
    print("- Admin: admin / admin123")
    print("- Bibliothécaire: biblio / biblio123")
    print("- Membre: membre / membre123")

if __name__ == "__main__":
    create_test_users()