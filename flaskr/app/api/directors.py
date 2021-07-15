"""Endpoint for directors"""


from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.models import Director
from app.api.auth import token_auth


@bp.route('/directors/<int:item_id>', methods=['GET'])
def get_director(item_id):
    """Get director using id or 404"""
    return jsonify(Director.query.get_or_404(item_id).to_dict())


@bp.route('/directors', methods=['GET'])
def get_directors():
    """Get all directors with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Director.to_collection_dict(Director.query, page, per_page, 'api.get_directors')
    return jsonify(data)


@bp.route('/directors/<int:item_id>/movies', methods=['GET'])
def get_director_movies(item_id):
    """Find all movies filmed by director using id with pagination"""
    director = Director.query.get_or_404(item_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Director.to_collection_dict(director.directed, page, per_page,
                                       'api.get_director_movies', item_id=item_id)
    return jsonify(data)


@bp.route('/directors', methods=['POST'])
@token_auth.login_required
def create_director():
    """Create director from post request"""
    data = request.get_json() or {}
    if 'f_name' not in data or 'l_name' not in data:
        return bad_request('Must include f_name and l_name')
    if Director.query.filter_by(f_name=data['f_name'], l_name=data['l_name']).first():
        return bad_request('This director already exists')

    director = Director()
    director.from_dict(data)

    db.session.add(director)
    response = jsonify(director.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_director', item_id=director.id)
    db.session.commit()
    return response


@bp.route('/directors/<int:item_id>', methods=['PUT'])
@token_auth.login_required
def update_director(item_id):
    """Change any parameter of director except id or return 404"""
    director = Director.query.get_or_404(item_id)
    data = request.get_json() or {}
    if 'f_name' in data and 'l_name' in data and\
            data['f_name'] != director.f_name and data['l_name'] != director.l_name and\
            Director.query.filter_by(f_name=data['f_name'], l_name=data['l_name']).first():
        return bad_request('Please use a different username')
    director.from_dict(data)
    db.session.commit()
    return jsonify(director.to_dict())


@bp.route('/directors/<int:item_id>', methods=['DELETE'])
@token_auth.login_required
def delete_director(item_id):
    """Delete director using id or return 404"""
    director = Director.query.get_or_404(item_id)
    db.session.delete(director)
    db.session.commit()
    return jsonify(director.to_dict())
