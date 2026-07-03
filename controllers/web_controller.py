import socket
from flask import Blueprint, render_template
from services.libro_service import LibroService
from services.estudiante_service import EstudianteService
from services.prestamo_service import PrestamoService

web_bp = Blueprint('web', __name__)

libro_service = LibroService()
estudiante_service = EstudianteService()
prestamo_service = PrestamoService()

@web_bp.route('/')
def index():
    # Obtener estadísticas básicas
    libros = libro_service.obtener_todos()
    estudiantes = estudiante_service.obtener_todos()
    prestamos = prestamo_service.obtener_todos()
    
    total_titulos = len(libros)
    total_inventario = sum(l.cantidad for l in libros)
    total_estudiantes = len(estudiantes)
    
    prestamos_activos = [p for p in prestamos if p.estado == 'prestado']
    total_prestados = len(prestamos_activos)
    
    # Obtener los 5 préstamos más recientes
    prestamos_recientes = sorted(prestamos, key=lambda x: x.id, reverse=True)[:5]
    
    hostname = socket.gethostname()
    
    return render_template(
        'index.html',
        total_titulos=total_titulos,
        total_inventario=total_inventario,
        total_estudiantes=total_estudiantes,
        total_prestados=total_prestados,
        prestamos_recientes=prestamos_recientes,
        hostname=hostname
    )

@web_bp.route('/libros')
def libros():
    libros = libro_service.obtener_todos()
    return render_template('libros.html', libros=libros)

@web_bp.route('/estudiantes')
def estudiantes():
    estudiantes = estudiante_service.obtener_todos()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@web_bp.route('/prestamos')
def prestamos():
    prestamos = prestamo_service.obtener_todos()
    libros = libro_service.obtener_todos()
    estudiantes = estudiante_service.obtener_todos()
    
    # Filtrar solo libros que tengan unidades disponibles
    libros_disponibles = [l for l in libros if l.disponibles > 0]
    
    return render_template(
        'prestamos.html',
        prestamos=prestamos,
        libros=libros_disponibles,
        estudiantes=estudiantes
    )
