import os
from flask import Flask, render_template
from config import Config, TestingConfig
from models.database import db
from controllers.web_controller import web_bp
from controllers.api_libro import api_libro_bp
from controllers.api_estudiante import api_estudiante_bp
from controllers.api_prestamo import api_prestamo_bp
from utils.errors import APIError
from utils.responses import json_error
from utils.logger import logger

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Seleccionar configuración
    if config_class is None:
        env = os.getenv("FLASK_ENV", "development")
        if env == "testing":
            config_class = TestingConfig
        else:
            config_class = Config
            
    app.config.from_object(config_class)
    
    # Inicializar Base de Datos
    db.init_app(app)
    
    # Registrar Blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_libro_bp)
    app.register_blueprint(api_estudiante_bp)
    app.register_blueprint(api_prestamo_bp)
    
    # Manejo de excepciones personalizadas de la API
    @app.errorhandler(APIError)
    def handle_api_error(error):
        logger.warning(f"API Error: {error.message} (Status: {error.status_code})")
        return json_error(error.message, error.status_code)
        
    # Manejo general de errores web
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal Server Error: {str(error)}")
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Crear tablas automáticamente al arrancar
    with app.app_context():
        try:
            db.create_all()
            logger.info("Base de datos y tablas inicializadas correctamente.")
        except Exception as e:
            logger.error(f"No se pudo inicializar la base de datos: {str(e)}")

    return app

app = create_app()

if __name__ == "__main__":
    # Configurar puerto y host por defecto para desarrollo
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(host=host, port=port, debug=True)
