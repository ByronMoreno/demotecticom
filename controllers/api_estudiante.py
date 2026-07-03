from flask import Blueprint, request
from services.estudiante_service import EstudianteService
from utils.responses import json_success

api_estudiante_bp = Blueprint('api_estudiante', __name__, url_prefix='/api/estudiantes')
estudiante_service = EstudianteService()

@api_estudiante_bp.route('', methods=['GET'])
def get_estudiantes():
    estudiantes = estudiante_service.obtener_todos()
    return json_success([estudiante.to_dict() for estudiante in estudiantes])

@api_estudiante_bp.route('/<int:estudiante_id>', methods=['GET'])
def get_estudiante(estudiante_id):
    estudiante = estudiante_service.obtener_por_id(estudiante_id)
    return json_success(estudiante.to_dict())

@api_estudiante_bp.route('', methods=['POST'])
def create_estudiante():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    email = data.get('email')
    codigo = data.get('codigo')
    
    estudiante = estudiante_service.crear_estudiante(nombre, email, codigo)
    return json_success(estudiante.to_dict(), "Estudiante creado exitosamente", 201)

@api_estudiante_bp.route('/<int:estudiante_id>', methods=['PUT'])
def update_estudiante(estudiante_id):
    data = request.get_json() or {}
    nombre = data.get('nombre')
    email = data.get('email')
    codigo = data.get('codigo')
    
    estudiante = estudiante_service.actualizar_estudiante(estudiante_id, nombre, email, codigo)
    return json_success(estudiante.to_dict(), "Estudiante actualizado exitosamente")

@api_estudiante_bp.route('/<int:estudiante_id>', methods=['DELETE'])
def delete_estudiante(estudiante_id):
    estudiante_service.eliminar_estudiante(estudiante_id)
    return json_success(message="Estudiante eliminado exitosamente")
