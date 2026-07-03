from models.estudiante import Estudiante
from .base_repository import BaseRepository

class EstudianteRepository(BaseRepository):
    def __init__(self):
        super().__init__(Estudiante)

    def find_by_codigo(self, codigo):
        return Estudiante.query.filter_by(codigo=codigo).first()

    def find_by_email(self, email):
        return Estudiante.query.filter_by(email=email).first()
