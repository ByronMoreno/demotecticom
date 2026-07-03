from datetime import date
from .database import db

class Prestamo(db.Model):
    __tablename__ = 'prestamos'

    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    fecha_prestamo = db.Column(db.Date, nullable=False, default=date.today)
    fecha_devolucion = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default='prestado')  # 'prestado' o 'devuelto'

    # Relationships
    libro = db.relationship('Libro', backref=db.backref('prestamos', lazy=True))
    estudiante = db.relationship('Estudiante', backref=db.backref('prestamos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'libro_id': self.libro_id,
            'libro_titulo': self.libro.titulo if self.libro else None,
            'estudiante_id': self.estudiante_id,
            'estudiante_nombre': self.estudiante.nombre if self.estudiante else None,
            'fecha_prestamo': self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            'fecha_devolucion': self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
            'estado': self.estado
        }
