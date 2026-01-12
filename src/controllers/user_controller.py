from src.models.database import Session, UtilisateurSys, Role, UtilisateurRole


class UserController:
    def __init__(self):
        self.session = Session()

    def create_utilisateur(self, username: str, password: str, role_libelle: str = None):
        user = UtilisateurSys(username=username, password=password)
        self.session.add(user)
        self.session.commit()
        if role_libelle:
            role = self.session.query(Role).filter_by(libelle=role_libelle).first()
            if role:
                assoc = UtilisateurRole(utilisateur_id=user.id, role_id=role.id)
                self.session.add(assoc)
                self.session.commit()
        return user

    def list_users(self):
        return self.session.query(UtilisateurSys).all()

    def deactivate_user(self, user_id: int):
        u = self.session.query(UtilisateurSys).get(user_id)
        if u:
            u.est_actif = False
            self.session.commit()
            return u
        return None
