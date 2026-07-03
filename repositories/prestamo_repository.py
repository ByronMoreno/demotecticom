from models.prestamo import Prestamo
from .base_repository import BaseRepository

class PrestamoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Prestamo)

    def find_active_by_estudiante(self, estudiante_id):
        return Prestamo.query.filter_by(estudiante_id=estudiante_id, estado='prestado').all()

    def find_active_by_libro(self, libro_id):
        return Prestamo.query.filter_by(libro_id=libro_id, estado='prestado').all()

    def find_active(self):
        return Prestamo.query.filter_by(estado='prestado').all()
