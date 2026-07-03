import json
from models.estudiante import Estudiante

def test_crear_estudiante(client, app):
    payload = {
        "nombre": "Ana Gomez",
        "email": "ana.gomez@gmail.com",
        "codigo": "EST-12345"
    }
    response = client.post('/api/estudiantes', data=json.dumps(payload), content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['nombre'] == "Ana Gomez"
    assert data['data']['codigo'] == "EST-12345"

def test_crear_estudiante_duplicado_email(client, app):
    payload1 = {
        "nombre": "Ana Gomez",
        "email": "ana@gmail.com",
        "codigo": "EST-11"
    }
    payload2 = {
        "nombre": "Ana Perez",
        "email": "ana@gmail.com",
        "codigo": "EST-22"
    }
    
    # Crear primero
    client.post('/api/estudiantes', data=json.dumps(payload1), content_type='application/json')
    # Crear segundo con mismo email
    response = client.post('/api/estudiantes', data=json.dumps(payload2), content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 409
    assert data['status'] == 'error'
