"""Endpoint for genres"""


from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.models import Genre
from app.api.auth import token_auth


@bp.route('/genres/<int:item_id>', methods=['GET'])
def get_genre(item_id):
    """Get genre using id or 404"""
    return jsonify(Genre.query.get_or_404(item_id).to_dict())


@bp.route('/genres', methods=['GET'])
def get_genres():
    """Get all genres with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Genre.to_collection_dict(Genre.query, page, per_page, 'api.get_genres')
    return jsonify(data)


@bp.route('/genres/<int:item_id>/movies', methods=['GET'])
def get_genre_movies(item_id):
    """Find all movies related to genre by id with pagination"""
    genre = Genre.query.get_or_404(item_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Genre.to_collection_dict(genre.movies, page, per_page,
                                    'api.get_genre_movies', item_id=item_id)
    return jsonify(data)


@bp.route('/genres', methods=['POST'])
@token_auth.login_required
def create_genre():
    """Create new genre from post request"""
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
    response.headers['Location'] = url_for('api.get_user', item_id=genre.id)
    return response


@bp.route('/genres/<int:item_id>', methods=['PUT'])
@token_auth.login_required
def update_genre(item_id):
    """Change genre name or 404"""
    user = Genre.query.get_or_404(item_id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.name and \
            Genre.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different genre name')
    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/genres/<int:item_id>', methods=['DELETE'])
@token_auth.login_required
def delete_genre(item_id):
    """Delete genre using id or 404"""
    genre = Genre.query.get_or_404(item_id)
    db.session.delete(genre)
    db.session.commit()
    return jsonify(genre.to_dict())
