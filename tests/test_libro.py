import json
from models.libro import Libro

def test_crear_libro(client, app):
    # Enviar solicitud POST para crear un libro
    payload = {
        "titulo": "Pruebas de Software",
        "autor": "John Doe",
        "isbn": "123-4567890",
        "cantidad": 5
    }
    response = client.post('/api/libros', data=json.dumps(payload), content_type='application/json')
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['titulo'] == "Pruebas de Software"
    assert data['data']['disponibles'] == 5

def test_crear_libro_duplicado(client, app):
    payload = {
        "titulo": "Libro Original",
        "autor": "Autor A",
        "isbn": "999-99999",
        "cantidad": 2
    }
    # Crear el primero
    response1 = client.post('/api/libros', data=json.dumps(payload), content_type='application/json')
    assert response1.status_code == 201
    
    # Intentar duplicar
    response2 = client.post('/api/libros', data=json.dumps(payload), content_type='application/json')
    data2 = json.loads(response2.data)
    
    assert response2.status_code == 409
    assert data2['status'] == 'error'

def test_obtener_libros(client, app):
    # Agregar un libro de forma directa
    with app.app_context():
        from models.database import db
        libro = Libro(titulo="Libro 1", autor="Autor 1", isbn="111", cantidad=3, disponibles=3)
        db.session.add(libro)
        db.session.commit()
        
    response = client.get('/api/libros')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data['data']) == 1
    assert data['data'][0]['titulo'] == "Libro 1"
