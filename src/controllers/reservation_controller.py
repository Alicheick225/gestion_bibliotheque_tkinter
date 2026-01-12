from src.models.database import Session, Reservation, Document, Membre
from datetime import datetime


class ReservationController:
    def __init__(self):
        self.session = Session()

    def create_reservation(self, membre_id: int, document_id: int):
        membre = self.session.query(Membre).get(membre_id)
        document = self.session.query(Document).get(document_id)
        if not membre or not document:
            return None
        res = Reservation(membre_id=membre_id, document_id=document_id, statut='En attente', date_reservation=datetime.now())
        self.session.add(res)
        self.session.commit()
        return res

    def list_reservations_for_member(self, membre_id: int):
        return self.session.query(Reservation).filter_by(membre_id=membre_id).all()

    def cancel_reservation(self, reservation_id: int):
        r = self.session.query(Reservation).get(reservation_id)
        if r:
            r.statut = 'Annulée'
            self.session.commit()
            return r
        return None
