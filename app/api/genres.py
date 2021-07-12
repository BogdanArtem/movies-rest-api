from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.models import Genre
from app.api.auth import token_auth


@bp.route('/genres/<int:id>', methods=['GET'])
def get_genre(id):
    return jsonify(Genre.query.get_or_404(id).to_dict())


@bp.route('/genres', methods=['GET'])
def get_genres():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Genre.to_collection_dict(Genre.query, page, per_page, 'api.get_genres')
    return jsonify(data)


@bp.route('/genres/<int:id>/movies', methods=['GET'])
def get_genre_movies(id):
    genre = Genre.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Genre.to_collection_dict(genre.movies, page, per_page, 'api.get_genre_movies', id=id)
    return jsonify(data)


@bp.route('/genres', methods=['POST'])
@token_auth.login_required
def create_genre():
    data = request.get_json() or {}
    if 'name' not in data:
        return bad_request('Must include name')
    if Genre.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')

    genre = Genre()
    genre.from_dict(data)

    db.session.add(genre)
    db.session.commit()
    response = jsonify(genre.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=genre.genre_id)
    return response


@bp.route('/genres/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_genre(id):
    user = Genre.query.get_or_404(id)
    data = request.get_json() or {}
    # if 'username' in data and data['username'] != user.username and \
    #         Genre.query.filter_by(username=data['username']).first():
    #     return bad_request('Please use a different username')
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/genres/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_genre(id):
    genre = Genre.query.get_or_404(id)
    db.session.delete(genre)
    db.session.commit()
    return jsonify(genre.to_dict())
