# Fichier: src/controllers/book_controller.py
from src.models.database import Session, Document

class DocumentController:
    def __init__(self):
        self.session = Session()

    def get_all_documents(self):
        """Récupère tous les documents"""
        return self.session.query(Document).all()

    def search_documents(self, query):
        """Recherche par titre ou ISBN"""
        # Attention : on utilise 'titre' (français) et non plus 'title'
        return self.session.query(Document).filter(
            (Document.titre.ilike(f'%{query}%')) | 
            (Document.isbn.ilike(f'%{query}%'))
        ).all()

    def add_document(self, titre, annee, isbn):
        """Ajout simplifié d'un document"""
        new_doc = Document(titre=titre, annee_publication=annee, isbn=isbn)
        self.session.add(new_doc)
        self.session.commit()

    def delete_document(self, doc_id):
        doc = self.session.query(Document).get(doc_id)
        if doc:
            self.session.delete(doc)
            self.session.commit()