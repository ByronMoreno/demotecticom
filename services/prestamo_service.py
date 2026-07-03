from datetime import date
from models.prestamo import Prestamo
from repositories.prestamo_repository import PrestamoRepository
from repositories.libro_repository import LibroRepository
from repositories.estudiante_repository import EstudianteRepository
from utils.errors import BadRequestError, NotFoundError

class PrestamoService:
    def __init__(self):
        self.prestamo_repo = PrestamoRepository()
        self.libro_repo = LibroRepository()
        self.estudiante_repo = EstudianteRepository()

    def obtener_todos(self):
        return self.prestamo_repo.get_all()

    def prestar_libro(self, libro_id, estudiante_id):
        libro = self.libro_repo.get_by_id(libro_id)
        if not libro:
            raise NotFoundError(f"Libro con ID {libro_id} no encontrado")

        estudiante = self.estudiante_repo.get_by_id(estudiante_id)
        if not estudiante:
            raise NotFoundError(f"Estudiante con ID {estudiante_id} no encontrado")

        if libro.disponibles <= 0:
            raise BadRequestError("No hay copias disponibles de este libro para préstamo")

        # Evitar préstamo duplicado activo para el mismo libro y estudiante
        active_loans = self.prestamo_repo.find_active_by_estudiante(estudiante_id)
        for loan in active_loans:
            if loan.libro_id == libro_id:
                raise BadRequestError("El estudiante ya tiene un préstamo activo de este mismo libro")

        prestamo = Prestamo(
            libro_id=libro_id,
            estudiante_id=estudiante_id,
            fecha_prestamo=date.today(),
            estado='prestado'
        )
        
        # Actualizar disponibles
        libro.disponibles -= 1
        self.libro_repo.update(libro)
        
        return self.prestamo_repo.create(prestamo)

    def devolver_libro(self, prestamo_id):
        prestamo = self.prestamo_repo.get_by_id(prestamo_id)
        if not prestamo:
            raise NotFoundError(f"Préstamo con ID {prestamo_id} no encontrado")

        if prestamo.estado == 'devuelto':
            raise BadRequestError("Este préstamo ya fue devuelto anteriormente")

        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion = date.today()

        # Incrementar disponibles en libro
        libro = self.libro_repo.get_by_id(prestamo.libro_id)
        if libro:
            libro.disponibles += 1
            if libro.disponibles > libro.cantidad:
                libro.disponibles = libro.cantidad
            self.libro_repo.update(libro)

        return self.prestamo_repo.update(prestamo)
