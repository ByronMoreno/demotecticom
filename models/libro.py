from .database import db

class Libro(db.Model):
    __tablename__ = 'libros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    disponibles = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'cantidad': self.cantidad,
            'disponibles': self.disponibles
        }
