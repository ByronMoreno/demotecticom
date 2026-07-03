from flask import Blueprint, request
from services.prestamo_service import PrestamoService
from utils.responses import json_success

api_prestamo_bp = Blueprint('api_prestamo', __name__, url_prefix='/api/prestamos')
prestamo_service = PrestamoService()

@api_prestamo_bp.route('', methods=['GET'])
def get_prestamos():
    prestamos = prestamo_service.obtener_todos()
    return json_success([prestamo.to_dict() for prestamo in prestamos])

@api_prestamo_bp.route('', methods=['POST'])
def create_prestamo():
    data = request.get_json() or {}
    libro_id = data.get('libro_id')
    estudiante_id = data.get('estudiante_id')
    
    prestamo = prestamo_service.prestar_libro(libro_id, estudiante_id)
    return json_success(prestamo.to_dict(), "Préstamo registrado exitosamente", 201)

@api_prestamo_bp.route('/<int:prestamo_id>/devolver', methods=['POST'])
def devolver_prestamo(prestamo_id):
    prestamo = prestamo_service.devolver_libro(prestamo_id)
    return json_success(prestamo.to_dict(), "Libro devuelto exitosamente")
