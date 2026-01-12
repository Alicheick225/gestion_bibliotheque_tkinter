from src.models.database import Session, UtilisateurSys
from datetime import datetime
import hashlib


class AuthController:
    def __init__(self):
        self.session = Session()
        self.current_user = None

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create_user(self, username: str, password: str, est_actif=True):
        hashed = self._hash_password(password)
        user = UtilisateurSys(username=username, password=hashed, est_actif=est_actif)
        self.session.add(user)
        self.session.commit()
        return user

    def authenticate(self, username: str, password: str):
        hashed = self._hash_password(password)
        user = self.session.query(UtilisateurSys).filter_by(username=username).first()
        if user and user.password == hashed and user.est_actif:
            user.date_derniere_connexion = datetime.now()
            self.session.commit()
            self.current_user = user
            return user
        return None

    def logout(self):
        self.current_user = None

    def get_roles(self, user):
        if not user:
            return []
        try:
            return [assoc.role.libelle for assoc in user.roles_association if assoc.role]
        except Exception:
            return []

    def get_current_user_roles(self):
        return self.get_roles(self.current_user)
