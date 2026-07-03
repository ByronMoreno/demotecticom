import json
from models.libro import Libro
from models.estudiante import Estudiante

def test_flujo_prestamo_y_devolucion(client, app):
    # Setup: Registrar un libro y un estudiante
    with app.app_context():
        from models.database import db
        libro = Libro(titulo="Libro Test", autor="Autor Test", isbn="T123", cantidad=1, disponibles=1)
        estudiante = Estudiante(nombre="Estudiante Test", email="estudiante@test.com", codigo="EST-TEST")
        db.session.add(libro)
        db.session.add(estudiante)
        db.session.commit()
        
        libro_id = libro.id
        estudiante_id = estudiante.id

    # 1. Realizar préstamo
    payload = {
        "libro_id": libro_id,
        "estudiante_id": estudiante_id
    }
    response = client.post('/api/prestamos', data=json.dumps(payload), content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['estado'] == 'prestado'
    prestamo_id = data['data']['id']

    # Verificar que el stock de disponibles bajó a 0
    with app.app_context():
        libro_check = db.session.get(Libro, libro_id)
        assert libro_check.disponibles == 0

    # 2. Intentar prestar el mismo libro de nuevo (debe fallar por falta de copias)
    response_fail = client.post('/api/prestamos', data=json.dumps(payload), content_type='application/json')
    data_fail = json.loads(response_fail.data)
    assert response_fail.status_code == 400
    assert "no hay copias disponibles" in data_fail['message'].lower()

    # 3. Devolver libro
    response_dev = client.post(f'/api/prestamos/{prestamo_id}/devolver')
    data_dev = json.loads(response_dev.data)
    
    assert response_dev.status_code == 200
    assert data_dev['data']['estado'] == 'devuelto'

    # Verificar que el stock de disponibles volvió a 1
    with app.app_context():
        libro_check = db.session.get(Libro, libro_id)
        assert libro_check.disponibles == 1
