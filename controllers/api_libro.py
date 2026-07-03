from flask import Blueprint, request
from services.libro_service import LibroService
from utils.responses import json_success

api_libro_bp = Blueprint('api_libro', __name__, url_prefix='/api/libros')
libro_service = LibroService()

@api_libro_bp.route('', methods=['GET'])
def get_libros():
    libros = libro_service.obtener_todos()
    return json_success([libro.to_dict() for libro in libros])

@api_libro_bp.route('/<int:libro_id>', methods=['GET'])
def get_libro(libro_id):
    libro = libro_service.obtener_por_id(libro_id)
    return json_success(libro.to_dict())

@api_libro_bp.route('', methods=['POST'])
def create_libro():
    data = request.get_json() or {}
    titulo = data.get('titulo')
    autor = data.get('autor')
    isbn = data.get('isbn')
    cantidad = int(data.get('cantidad', 1))
    
    libro = libro_service.crear_libro(titulo, autor, isbn, cantidad)
    return json_success(libro.to_dict(), "Libro creado exitosamente", 201)

@api_libro_bp.route('/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    data = request.get_json() or {}
    titulo = data.get('titulo')
    autor = data.get('autor')
    isbn = data.get('isbn')
    cantidad = int(data.get('cantidad', 1))
    
    libro = libro_service.actualizar_libro(libro_id, titulo, autor, isbn, cantidad)
    return json_success(libro.to_dict(), "Libro actualizado exitosamente")

@api_libro_bp.route('/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    libro_service.eliminar_libro(libro_id)
    return json_success(message="Libro eliminado exitosamente")
