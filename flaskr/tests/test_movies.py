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
    req1 = client.get('/api/movies')
    req2 = client.get('/api/movies/1')
    req3 = client.get('/api/movies/2')
    req4 = client.get('/api/movies/3')

    assert '200' in req1.status
    assert '200' in req2.status
    assert '200' in req3.status
    assert '200' in req4.status


def test_add_new_movie(client):
    """Create new user by anonymous user"""
    movie = {
        'name': 'Awesome_movie',
        'director_id': '1',
        'date': '1999-01-01',
        'description': 'This movie is simply awesome',
        'rating': '5',
        'poster_url': 'www.poster.com',
        'user_id': '1'
    }

    # Unauthorized movie creation
    req1 = client.post(path='api/movies', json=movie)
    assert '401' in req1.status

    # Alex token
    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req2.json['token']

    # Create movie as Alex
    req3 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token}, json=movie)
    assert '201' in req3.status

    # Create the movie second time
    req4 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token}, json=movie)
    assert '400' in req4.status


def test_delete_movie(client):
    """Delete user using id"""
    # Unauthorized movie deletion
    req1 = client.delete(path='api/movies/1')
    assert '401' in req1.status

    movie = {
        'name': 'Go go go',
        'director_id': '1',
        'date': '1999-01-02',
        'description': 'This movie is simply awesome',
        'rating': '10',
        'poster_url': 'www.poster.com',
        'user_id': '1'  # Alex id
    }

    # Get tokens
    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token_alex = req2.json['token']

    req3 = client.post(path='api/tokens', auth=('Gim', 12345))
    token_gim = req3.json['token']

    # Create movie as Alex
    req4 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token_alex}, json=movie)
    assert '201' in req4.status
    id1 = req4.json['id']

    # Delete movie as Gim
    req5 = client.delete(path=f'api/movies/{id1}', headers={'Authorization': 'Bearer ' + token_gim})
    assert '403' in req5.status

    # Delete movie as Alex
    req6 = client.delete(path=f'api/movies/{id1}', headers={'Authorization': 'Bearer ' + token_alex})
    assert '200' in req6.status

    # Create movie as Alex
    req7 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token_alex}, json=movie)
    assert '201' in req7.status
    id2 = req7.json['id']

    # Delete movie as Admin
    req8 = client.post(path='api/tokens', auth=('Admin', 12345))
    token_admin = req8.json['token']
    req9 = client.delete(path=f'api/movies/{id2}', headers={'Authorization': 'Bearer ' + token_admin})
    assert '200' in req9.status


def test_update_movie(client):
    """Update user using id"""
    # Unauthorized movie deletion
    req1 = client.put(path='api/movies/1')
    assert '401' in req1.status

    movie = {
        'name': 'Go go go',
        'director_id': '1',
        'date': '1999-01-02',
        'description': 'This movie is simply awesome',
        'rating': '10',
        'poster_url': 'www.poster.com',
        'user_id': '1'  # Alex id
    }

    # Get tokens
    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token_alex = req2.json['token']

    req3 = client.post(path='api/tokens', auth=('Gim', 12345))
    token_gim = req3.json['token']

    # Create movie as Alex
    req4 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token_alex}, json=movie)
    assert '201' in req4.status
    id1 = req4.json['id']

    # Update movie as Gim
    req5 = client.put(path=f'api/movies/{id1}', headers={'Authorization': 'Bearer ' + token_gim})
    assert '403' in req5.status

    # Update movie as Alex
    req6 = client.put(path=f'api/movies/{id1}', headers={'Authorization': 'Bearer ' + token_alex})
    assert '200' in req6.status

    # Update movie as Admin
    req7 = client.post(path='api/tokens', auth=('Admin', 12345))
    token_admin = req7.json['token']
    req8 = client.put(path=f'api/movies/{id1}', headers={'Authorization': 'Bearer ' + token_admin})
    assert '200' in req8.status


def test_rating_constraint(client):
    """Check rating is in range from 0 to 10"""
    movie = {
        'name': 'Go go go',
        'director_id': '1',
        'date': '1999-01-02',
        'description': 'This movie is simply awesome',
        'rating': '15',
        'poster_url': 'www.poster.com',
        'user_id': '1'  # Alex id
    }

    # Get tokens
    req2 = client.post(path='api/tokens', auth=('Alex', 12345))
    token_alex = req2.json['token']

    # Create movie as Alex
    req3 = client.post(path='api/movies', headers={'Authorization': 'Bearer ' + token_alex}, json=movie)
    assert '400' in req3.status


def test_add_same_users(client):
    """Create movies with same names"""

    movie = {
        'name': 'Twilight',
        'director_id': '1',
        'date': '1999-01-02',
        'description': 'This movie is simply awesome',
        'rating': '9',
        'poster_url': 'www.poster.com',
        'user_id': '1'  # Alex id
    }

    # Get tokens
    req1 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req1.json['token']

    req2 = client.post('api/movies', json=movie, headers={'Authorization': 'Bearer ' + token})
    print(req2.json)
    assert '201' in req2.status

    req3 = client.post('api/movies', json=movie, headers={'Authorization': 'Bearer ' + token})
    assert '400' in req3.status


def test_director_deletion(client):
    """Delete director for existing movie"""
    # Get tokens
    req1 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req1.json['token']

    # Delete director and check movie
    req2 = client.get('api/directors/2')
    assert '200' in req2.status
    req3 = client.delete(path='api/directors/2', headers={'Authorization': 'Bearer ' + token})
    req4 = client.get('api/movies/1')

    assert 'unknown' in req4.json['_links']['director']


def test_user_deletion(client):
    """Delete user for existing movie"""
    # Get tokens
    req1 = client.post(path='api/tokens', auth=('Alex', 12345))
    token = req1.json['token']

    # Delete director and check movie
    req2 = client.get('api/users/2')
    assert '200' in req2.status
    req3 = client.delete(path='api/users/2', headers={'Authorization': 'Bearer ' + token})
    req4 = client.get('api/movies/1')

    assert 'unknown' in req4.json['_links']['user']