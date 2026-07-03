from models.libro import Libro
from repositories.libro_repository import LibroRepository
from repositories.prestamo_repository import PrestamoRepository
from utils.errors import BadRequestError, NotFoundError, ConflictError

class LibroService:
    def __init__(self):
        self.libro_repo = LibroRepository()
        self.prestamo_repo = PrestamoRepository()

    def obtener_todos(self):
        return self.libro_repo.get_all()

    def obtener_por_id(self, libro_id):
        libro = self.libro_repo.get_by_id(libro_id)
        if not libro:
            raise NotFoundError(f"Libro con ID {libro_id} no encontrado")
        return libro

    def crear_libro(self, titulo, autor, isbn, cantidad):
        if not titulo or not autor or not isbn:
            raise BadRequestError("El título, autor e ISBN son campos obligatorios")
        
        if cantidad < 0:
            raise BadRequestError("La cantidad no puede ser negativa")

        existing_libro = self.libro_repo.find_by_isbn(isbn)
        if existing_libro:
            raise ConflictError(f"El libro con ISBN {isbn} ya está registrado")

        libro = Libro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            cantidad=cantidad,
            disponibles=cantidad
        )
        return self.libro_repo.create(libro)

    def actualizar_libro(self, libro_id, titulo, autor, isbn, cantidad):
        libro = self.obtener_por_id(libro_id)

        if not titulo or not autor or not isbn:
            raise BadRequestError("El título, autor e ISBN son campos obligatorios")

        if cantidad < 0:
            raise BadRequestError("La cantidad no puede ser negativa")

        if libro.isbn != isbn:
            existing_libro = self.libro_repo.find_by_isbn(isbn)
            if existing_libro:
                raise ConflictError(f"El libro con ISBN {isbn} ya está registrado")

        # Calcular diferencia en la cantidad para actualizar los disponibles
        diff = cantidad - libro.cantidad
        nuevos_disponibles = libro.disponibles + diff
        if nuevos_disponibles < 0:
            raise BadRequestError("La nueva cantidad es inconsistente con los préstamos activos actualmente")

        libro.titulo = titulo
        libro.autor = autor
        libro.isbn = isbn
        libro.cantidad = cantidad
        libro.disponibles = nuevos_disponibles

        return self.libro_repo.update(libro)

    def eliminar_libro(self, libro_id):
        libro = self.obtener_por_id(libro_id)
        
        # Validar si tiene préstamos activos
        active_loans = self.prestamo_repo.find_active_by_libro(libro_id)
        if active_loans:
            raise BadRequestError("No se puede eliminar el libro porque tiene préstamos activos")

        # Eliminar préstamos devueltos históricos asociados
        for prestamo in libro.prestamos:
            self.prestamo_repo.delete(prestamo)

        self.libro_repo.delete(libro)
        return True
