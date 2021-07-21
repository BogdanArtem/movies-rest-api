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
    req1 = client.get('/api/genres')
    req2 = client.get('/api/genres/1')
    req3 = client.get('/api/genres/2')
    req4 = client.get('/api/genres/3')

    assert '200' in req1.status
    assert '200' in req2.status
    assert '200' in req3.status
    assert '200' in req4.status


def test_add_new_genre(client):
    """Create new genre by anonymous user"""
    req1 = client.post(path='api/genres', json={'name': 'Fantasy'})
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']
    req3 = client.post(path='api/genres', json={'name': 'Fantasy'},
                       headers={'Authorization': 'Bearer ' + token})
    assert '201' in req3.status


def test_delete_genre(client):
    """Delete genre by id"""
    req1 = client.delete(path='api/genres/1')
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']
    req3 = client.delete(path='api/genres/1', headers={'Authorization': 'Bearer ' + token})
    assert '200' in req3.status


def test_update_genre(client):
    """Upadate user using id"""
    data = {'name': 'Horror'}
    req1 = client.put(path='api/genres/2', json=data)
    assert '401' in req1.status

    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']
    req3 = client.put(path='api/genres/2', headers={'Authorization': 'Bearer ' + token}, json=data)
    assert '200' in req3.status


def test_add_same_genre(client):
    """Create users with same email and username"""
    genre = {'name': 'Cars'}

    req1 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req1.json['token']

    req2 = client.post('api/genres', headers={'Authorization': 'Bearer ' + token}, json=genre)
    assert '201' in req2.status

    # Add user with repeating username
    req3 = client.post('api/genres', headers={'Authorization': 'Bearer ' + token}, json=genre)
    assert '409' in req3.status


def test_many_to_many(client):
    """Check many to many relationship between genre and movie"""
    req1 = client.get('api/genres/1')
    assert '200' in req1.status
    assert 2 == req1.json['movies_count']

    req2 = client.get('api/genres/3')
    assert '200' in req2.status
    assert 1 == req2.json['movies_count']

    movie1 = {
        'name': 'Twilight',
        'director_id': '1',
        'date': '1999-01-02',
        'description': 'This movie is simply awesome',
        'rating': '9',
        'poster_url': 'www.poster.com',
        'user_id': '1',  # Alex id
        'genres': ['1', '3']
    }

    # Get tokens
    req3 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req3.json['token']

    req4 = client.post('api/movies', headers={'Authorization': 'Bearer ' + token}, json=movie1)
    assert '201' in req4.status

    req5 = client.get('api/genres/1')
    assert '200' in req5.status
    assert 3 == req5.json['movies_count'] # +1

    req6 = client.get('api/genres/3')
    assert '200' in req6.status
    assert 2 == req6.json['movies_count'] # +1

    req7 = client.get('api/users/5')
    assert '401' in req7.status
