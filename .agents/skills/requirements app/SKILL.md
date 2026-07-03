# Sistema de Biblioteca (BiblioSwarm)

Este es un sistema completo de gestión de biblioteca listo para producción, desarrollado con **Flask (Python 3.14)**, **PostgreSQL**, **Docker Swarm**, **Traefik** y **GitHub Actions CI/CD**. 

El proyecto implementa una arquitectura por capas siguiendo principios **SOLID**, **Clean Code** y **PEP 8**. Ofrece un panel de control web responsivo e interactivo diseñado con una estética moderna (glassmorfismo y Bootstrap 5) y una API RESTful que responde en formato JSON.

---

## 📂 Estructura del Proyecto

```text
proyecto/
├── app.py                      # Punto de entrada de la aplicación y registro de Blueprints
├── config.py                   # Configuración del entorno (Desarrollo, Pruebas, Producción)
├── requirements.txt            # Dependencias del proyecto
├── Dockerfile                  # Empaquetado Docker de producción (multi-hilo)
├── .dockerignore               # Archivos omitidos en la compilación de la imagen Docker
├── Makefile                    # Comandos de automatización para Docker Swarm
├── stack.yml                   # Orquestación Docker Swarm
├── .gitignore                  # Exclusiones de Git
│
├── controllers/                # Controladores de Rutas y Blueprints
│   ├── web_controller.py       # Renderizado de vistas HTML (Jinja2)
│   ├── api_libro.py            # CRUD de la API REST para Libros
│   ├── api_estudiante.py       # CRUD de la API REST para Estudiantes
│   └── api_prestamo.py         # CRUD de la API REST para Préstamos
│
├── services/                   # Capa de Lógica de Negocio y Validaciones
│   ├── libro_service.py
│   ├── estudiante_service.py
│   └── prestamo_service.py
│
├── repositories/               # Capa de Acceso a Datos (SQLAlchemy)
│   ├── base_repository.py      # Repositorio genérico CRUD
│   ├── libro_repository.py
│   ├── estudiante_repository.py
│   └── prestamo_repository.py
│
├── models/                     # Modelos de Base de Datos
│   ├── database.py             # Instancia SQLAlchemy compartida
│   ├── libro.py
│   ├── estudiante.py
│   └── prestamo.py
│
├── static/                     # Archivos Estáticos (Estilo Glassmórfico)
│   └── css/
│       └── custom.css
│
├── templates/                  # Vistas Jinja2 (Bootstrap 5)
│   ├── base.html
│   ├── index.html              # Dashboard principal
│   ├── libros.html             # CRUD de libros
│   ├── estudiantes.html        # CRUD de estudiantes
│   ├── prestamos.html          # CRUD de préstamos
│   └── errors/
│       ├── 404.html            # Error 404 personalizado
│       └── 500.html            # Error 500 personalizado
│
├── utils/                      # Utilidades
│   ├── errors.py               # Excepciones personalizadas HTTP
│   ├── logger.py               # Configuración de registro (Logging)
│   └── responses.py            # Formato estándar de respuestas JSON
│
└── tests/                      # Suite de Pruebas Unitarias e Integración
    ├── conftest.py             # Accesorios (Fixtures) de Pytest
    ├── test_libro.py
    ├── test_estudiante.py
    └── test_prestamo.py
```

---

## 🛠️ Instalación y Ejecución Local

### Prerrequisitos
- Python 3.10 o superior (recomendado 3.14-slim para producción)
- PostgreSQL (si deseas usar base de datos física localmente)

### Pasos
1. **Clonar el repositorio**:
   ```bash
   git clone <URL_REPOSITORIO>
   cd demo_ia
   ```

2. **Crear e iniciar un entorno virtual**:
   ```bash
   python -m venv venv
   # En Windows (Powershell)
   .\venv\Scripts\Activate.ps1
   # En Linux / macOS
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**:
   Crea un archivo `.env` a partir del ejemplo:
   ```bash
   cp .env.example .env
   ```
   Ajusta los valores del archivo `.env` para conectar con tu PostgreSQL local:
   ```env
   FLASK_ENV=development
   SECRET_KEY=clave_secreta_desarrollo
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=tu_password
   POSTGRES_DB=biblioteca
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Ejecutar Pruebas Automatizadas**:
   ```bash
   python -m pytest
   ```

6. **Iniciar el servidor local**:
   ```bash
   python app.py
   ```
   La aplicación estará disponible en `http://localhost:5000`.

---

## 🛢️ Configuración de PostgreSQL en Producción
El sistema crea automáticamente el esquema de tablas en el arranque (`db.create_all()`) si las tablas no existen. En producción, el contenedor de base de datos se ejecuta como parte del servicio de Docker Swarm, aprovisionado con un volumen persistente `pgdata`.

---

## 🐳 Docker
Para construir y probar la imagen Docker localmente:
```bash
# Construir la imagen
docker build -t ghcr.io/byronmoreno/practica:1.0.0 .

# Ejecutar el contenedor
docker run -d -p 5000:5000 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=secreto \
  -e DATABASE_URL=sqlite:///:memory: \
  ghcr.io/byronmoreno/practica:1.0.0
```

---

## 🕸️ Docker Swarm y Traefik
El despliegue en producción utiliza **Docker Swarm** detrás de un proxy inverso **Traefik** que gestiona la terminación SSL con Let's Encrypt de forma automática.

### Despliegue con Makefile
Puedes utilizar las macros definidas en el `Makefile`:
```bash
# Compilar la imagen de producción
make build

# Subir la imagen al registro (GHCR)
make push

# Desplegar el stack en Swarm
make deploy

# Ver los logs del servicio
make logs

# Reiniciar el servicio web con rolling update
make restart

# Eliminar el stack de Swarm
make rm
```

El archivo `stack.yml` configura:
- 2 réplicas del contenedor web para alta disponibilidad.
- Configuración de actualización progresiva (rolling updates) con `delay: 10s` y rollback automático en caso de fallo.
- Enrutamiento por dominio a `practica.byronrm.com` mediante etiquetas de Traefik conectadas a la red `traefik-public`.

---

## 🚀 Integración y Despliegue Continuo (CI/CD)
El flujo de trabajo definido en `.github/workflows/deploy.yml` consta de dos etapas:

### Job 1: `build-and-push`
- Se activa al hacer push a las ramas `main` o `master`.
- Compila la imagen usando `docker/setup-buildx-action` y habilita el caché de GitHub Actions para compilaciones súper rápidas.
- Publica la imagen en GitHub Container Registry (`ghcr.io`) bajo tres etiquetas:
  1. `1.0.0`
  2. El hash corto de commit (`${{ github.sha }}`)
  3. `latest`

### Job 2: `deploy`
- Se ejecuta inmediatamente después de una compilación exitosa de la imagen.
- Crea el archivo `.env` dinámicamente usando secretos guardados en el repositorio de GitHub (`secrets.SECRET_KEY`, `secrets.POSTGRES_USER`, etc.).
- Transfiere los archivos `stack.yml` y `.env` al VPS usando protocolo SCP seguro (`appleboy/scp-action`).
- Inicia sesión SSH en el servidor (`appleboy/ssh-action`) y ejecuta los siguientes comandos de despliegue para levantar la infraestructura sin tiempo de inactividad:
  1. Login en el registro `ghcr.io`.
  2. Descarga la versión más reciente del contenedor.
  3. Exporta las variables del archivo `.env`.
  4. Ejecuta `docker stack deploy -c stack.yml practica`.
