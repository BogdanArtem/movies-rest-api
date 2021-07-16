"""Endpoint for movies"""


from flask import jsonify, request, url_for
from sqlalchemy.exc import IntegrityError
from app.api import bp
from app import db
from app.api.errors import bad_request, error_response
from app.models import Movie
from app.api.auth import token_auth


@bp.route('/movies/<int:item_id>', methods=['GET'])
def get_movie(item_id):
    """Get movie using id or 404"""
    return jsonify(Movie.query.get_or_404(item_id).to_dict())


@bp.route('/movies', methods=['GET'])
def get_movies():
    """Get all movies with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Movie.to_collection_dict(Movie.query, page, per_page, 'api.get_movies')
    return jsonify(data)


@bp.route('/movies/search/<string:inquiry>', methods=['GET'])
def search(inquiry):
    """Return all matches of name and description from elasticsearch index with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    matches, _ = Movie.search(inquiry, page, per_page)
    data = Movie.to_collection_dict(matches, page, per_page, 'api.search', inquiry=inquiry)
    return jsonify(data)


@bp.route('/movies/<int:item_id>/genres', methods=['GET'])
def get_movie_genres(item_id):
    """Find all genres related to movie with pagination"""
    movie = Movie.query.get_or_404(item_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Movie.to_collection_dict(movie.genres, page, per_page,
                                    'api.get_movie_genres', item_id=item_id)
    return jsonify(data)


@bp.route('/movies', methods=['POST'])
@token_auth.login_required
def create_movie():
    """Create movie with post request"""
    data = request.get_json() or {}
    if 'director_id' not in data or 'user_id' not in data or 'date' not in data or\
            'name' not in data or 'rating' not in data or 'poster_url' not in data:
        return bad_request('Must include user_id, director_id, '
                           'date, name, rating and poster_url fields')
    if Movie.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')

    movie = Movie()
    movie.from_dict(data)

    try:
        db.session.add(movie)
        db.session.commit()
    except IntegrityError:
        return bad_request("Please, check rating is in range from 1 to 10")

    db.session.commit()
    response = jsonify(movie.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_movie', item_id=movie.id)
    return response


@bp.route('/movies/<int:item_id>', methods=['PUT'])
@token_auth.login_required
def update_movie(item_id):
    """Change any of movies fields except id or 404"""
    movie = Movie.query.get_or_404(item_id)
    current_user = token_auth.current_user()
    data = request.get_json() or {}
    if 'name' in data and data['name'] != movie.name and \
            Movie.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')
    if movie.user_added is current_user or current_user.is_admin:
        movie.from_dict(data)
        db.session.commit()
        return jsonify(movie.to_dict())
    return error_response(403, "User updating this movie does not have right permissions")


@bp.route('/movies/<int:item_id>', methods=['DELETE'])
@token_auth.login_required
def delete_movie(item_id):
    """Delete movie or 404"""
    movie = Movie.query.get_or_404(item_id)
    current_user = token_auth.current_user()
    if movie.user_added is current_user or current_user.is_admin:
        db.session.delete(movie)
        db.session.commit()
        return jsonify(movie.to_dict())
    return error_response(403, "User deleting this movie does not have right permissions")
