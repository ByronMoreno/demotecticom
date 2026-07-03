from models.libro import Libro
from .base_repository import BaseRepository

class LibroRepository(BaseRepository):
    def __init__(self):
        super().__init__(Libro)

    def find_by_isbn(self, isbn):
        return Libro.query.filter_by(isbn=isbn).first()
