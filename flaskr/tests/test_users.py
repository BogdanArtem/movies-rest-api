import os
import base64
import pytest
from app.models import User, Director, Movie, Genre
from database import init_db
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
    req1 = client.get('/api/users')
    req2 = client.get('/api/users/1')
    req3 = client.get('/api/users/2')
    req4 = client.get('/api/users/3')

    assert '200' in req1.status
    assert '200' in req2.status
    assert '200' in req3.status
    assert '200' in req4.status


def test_register_new_user(client):
    """Create new user by anonymous user"""
    req = client.post(path='api/users', json={'username': 'new_user',
                                               'email': 'new_user@gmail.com', 'password': '12345'})
    assert '201' in req.status


def test_delete_user(client):
    """Delete user using id"""
    req1 = client.delete(path='api/users/1')
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']
    req3 = client.delete(path='api/users/1', headers={'Authorization': 'Bearer ' + token})
    assert '200' in req3.status


def test_update_user(client):
    """Upadate user using id"""
    data = {'username': 'Valera'}
    req1 = client.put(path='api/users/2', json=data)
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']
    req3 = client.put(path='api/users/2', headers={'Authorization': 'Bearer ' + token}, json=data)
    assert '200' in req3.status


def test_add_same_users(client):
    """Create users with same email and username"""
    user1 = {'username': 'Andy', 'email': 'andy@gmail.com', 'password': '12345'}
    user2 = {'username': 'Andy', 'email': '123andy@gmail.com', 'password': '12345'}

    req1 = client.post('api/users', json=user1)
    assert '201' in req1.status

    # Add user with repeating username
    req2 = client.post('api/users', json=user2)
    assert '400' in req2.status

    # Add user with repeating email
    user1['username'] = 'UniqueUsr'
    req3 = client.post('api/users', json=user1)
    assert '400' in req3.status
