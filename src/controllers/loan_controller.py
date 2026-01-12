from src.models.database import Session, Emprunt, Exemplaire, Membre
from datetime import datetime, timedelta


class LoanController:
    def __init__(self):
        self.session = Session()

    def create_emprunt(self, membre_id: int, exemplaire_id: int, utilisateur_emprunt_id: int):
        ex = self.session.query(Exemplaire).get(exemplaire_id)
        membre = self.session.query(Membre).get(membre_id)
        if not ex or not membre:
            return None
        if getattr(ex, 'statut', '').lower() != 'disponible':
            return None

        duree_days = membre.type_membre.duree_emprunt if membre.type_membre else 14
        date_retour_prevue = datetime.now().date() + timedelta(days=duree_days)

        emprunt = Emprunt(membre_id=membre_id, exemplaire_id=exemplaire_id,
                         utilisateur_emprunt_id=utilisateur_emprunt_id,
                         date_retour_prevue=date_retour_prevue)
        ex.statut = 'Emprunté'
        self.session.add(emprunt)
        self.session.commit()
        return emprunt

    def return_exemplaire(self, emprunt_id: int, utilisateur_retour_id: int):
        emprunt = self.session.query(Emprunt).get(emprunt_id)
        if not emprunt:
            return None
        emprunt.date_retour_reelle = datetime.now()
        emprunt.utilisateur_retour_id = utilisateur_retour_id
        # remettre l'exemplaire en disponible
        ex = emprunt.exemplaire
        if ex:
            ex.statut = 'Disponible'
        self.session.commit()
        return emprunt
