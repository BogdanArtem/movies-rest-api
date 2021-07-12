from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.models import Movie


@bp.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    print(id)
    return jsonify(Movie.query.get_or_404(id).to_dict())


@bp.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Movie.to_collection_dict(Movie.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/movies/<int:id>/genres', methods=['GET'])
def get_movie_genres(id):
    movie = Movie.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Movie.to_collection_dict(movie.genres, page, per_page, 'api.get_movie_genres', id=id)
    return jsonify(data)


@bp.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json() or {}
    if 'director_id' not in data or 'user_id' not in data or 'date' not in data or\
            'name' not in data or 'rating' not in data or 'poster_url' not in data:
        return bad_request('Must include user_id, director_id, date, name, rating and poster_url fields')
    if Movie.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')

    movie = Movie()
    movie.from_dict(data)

    db.session.add(movie)
    db.session.commit()
    response = jsonify(movie.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_movie', id=movie.movie_id)
    return response


@bp.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != movie.name and \
            Movie.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different username')
    movie.from_dict(data)
    db.session.commit()
    return jsonify(movie.to_dict())


@bp.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify(movie.to_dict())
