import os
import base64
import pytest
from app.models import User, Director, Movie, Genre
from app.dev_database import init_db
from app import create_app, db
from werkzeug.datastructures import Headers


@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            init_db()
            Movie.reindex()
        yield client
    os.remove('app/app.db')


def test_get_unauthorized(client):
    req1 = client.get('/api/directors')
    req2 = client.get('/api/directors/1')
    req3 = client.get('/api/directors/2')
    req4 = client.get('/api/directors/3')

    assert '200' in req1.status
    assert '200' in req2.status
    assert '200' in req3.status
    assert '200' in req4.status


def test_add_new_director(client):
    """Create new genre by anonymous user"""
    req1 = client.post(path='api/directors', json={'f_name': 'Jim', 'l_name': 'Berns'})
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Admin', 12345))
    token = req2.json['token']
    req3 = client.post(path='api/genres', json={'name': 'Fantasy'},
                       headers={'Authorization': 'Bearer ' + token})
    assert '201' in req3.status


def test_delete_genre(client):
    """Delete genre by id"""
    req1 = client.delete(path='api/genres/1')
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Admin', 12345))
    token = req2.json['token']
    req3 = client.delete(path='api/genres/1', headers={'Authorization': 'Bearer ' + token})
    assert '200' in req3.status


def test_update_genre(client):
    """Upadate user using id"""
    data = {'name': 'Horror'}
    req1 = client.put(path='api/genres/2', json=data)
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Admin', 12345))
    token = req2.json['token']
    req3 = client.put(path='api/genres/2', headers={'Authorization': 'Bearer ' + token}, json=data)
    assert '200' in req3.status


def test_add_same_genre(client):
    """Create users with same email and username"""
    data = {'name': 'Cars'}

    req1 = client.post(path='api/tokens', auth=('Admin', 12345))
    token = req1.json['token']

    req2 = client.post('api/genres', json=data, headers={'Authorization': 'Bearer ' + token})
    assert '201' in req2.status

    # Add user with repeating username
    req3 = client.post('api/genres', json=data, headers={'Authorization': 'Bearer ' + token})
    assert '409' in req3.status
