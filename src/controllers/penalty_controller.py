from src.models.database import Session, Penalite, Emprunt
from datetime import datetime


class PenaltyController:
    def __init__(self):
        self.session = Session()

    def compute_penalty_for_emprunt(self, emprunt_id: int):
        emprunt = self.session.query(Emprunt).get(emprunt_id)
        if not emprunt:
            return None
        if not emprunt.date_retour_reelle or not emprunt.date_retour_prevue:
            return None

        # compute days late
        days_late = (emprunt.date_retour_reelle.date() - emprunt.date_retour_prevue).days
        if days_late <= 0:
            return None

        taux = emprunt.membre.type_membre.taux_penalite_jour if emprunt.membre and emprunt.membre.type_membre else 0
        montant = days_late * (taux or 0)
        penalite = Penalite(montant_du=montant, montant_paye=0.0, motif='Retard', statut='Non payé', membre_id=emprunt.membre_id, emprunt_id=emprunt.id, utilisateur_creation_id=None)
        self.session.add(penalite)
        self.session.commit()
        return penalite
