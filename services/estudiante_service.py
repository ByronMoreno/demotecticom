from models.estudiante import Estudiante
from repositories.estudiante_repository import EstudianteRepository
from repositories.prestamo_repository import PrestamoRepository
from utils.errors import BadRequestError, NotFoundError, ConflictError

class EstudianteService:
    def __init__(self):
        self.estudiante_repo = EstudianteRepository()
        self.prestamo_repo = PrestamoRepository()

    def obtener_todos(self):
        return self.estudiante_repo.get_all()

    def obtener_por_id(self, estudiante_id):
        estudiante = self.estudiante_repo.get_by_id(estudiante_id)
        if not estudiante:
            raise NotFoundError(f"Estudiante con ID {estudiante_id} no encontrado")
        return estudiante

    def crear_estudiante(self, nombre, email, codigo):
        if not nombre or not email or not codigo:
            raise BadRequestError("El nombre, correo e identificador/código son campos obligatorios")

        if self.estudiante_repo.find_by_codigo(codigo):
            raise ConflictError(f"El estudiante con código {codigo} ya está registrado")

        if self.estudiante_repo.find_by_email(email):
            raise ConflictError(f"El estudiante con correo {email} ya está registrado")

        estudiante = Estudiante(
            nombre=nombre,
            email=email,
            codigo=codigo
        )
        return self.estudiante_repo.create(estudiante)

    def actualizar_estudiante(self, estudiante_id, nombre, email, codigo):
        estudiante = self.obtener_por_id(estudiante_id)

        if not nombre or not email or not codigo:
            raise BadRequestError("El nombre, correo e identificador/código son campos obligatorios")

        if estudiante.codigo != codigo:
            if self.estudiante_repo.find_by_codigo(codigo):
                raise ConflictError(f"El estudiante con código {codigo} ya está registrado")

        if estudiante.email != email:
            if self.estudiante_repo.find_by_email(email):
                raise ConflictError(f"El estudiante con correo {email} ya está registrado")

        estudiante.nombre = nombre
        estudiante.email = email
        estudiante.codigo = codigo

        return self.estudiante_repo.update(estudiante)

    def eliminar_estudiante(self, estudiante_id):
        estudiante = self.obtener_por_id(estudiante_id)
        
        # Validar si tiene préstamos activos
        active_loans = self.prestamo_repo.find_active_by_estudiante(estudiante_id)
        if active_loans:
            raise BadRequestError("No se puede eliminar al estudiante porque tiene préstamos activos")

        # Eliminar préstamos devueltos históricos asociados
        for prestamo in estudiante.prestamos:
            self.prestamo_repo.delete(prestamo)

        self.estudiante_repo.delete(estudiante)
        return True
