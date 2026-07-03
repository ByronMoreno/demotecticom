from models.database import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, entity_id):
        return db.session.get(self.model, entity_id)

    def get_all(self):
        return self.model.query.all()

    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity):
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
