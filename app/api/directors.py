from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.models import Director
from app.api.auth import token_auth


@bp.route('/directors/<int:id>', methods=['GET'])
def get_director(id):
    return jsonify(Director.query.get_or_404(id).to_dict())


@bp.route('/directors', methods=['GET'])
def get_directors():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Director.to_collection_dict(Director.query, page, per_page, 'api.get_directors')
    return jsonify(data)


@bp.route('/directors/<int:id>/movies', methods=['GET'])
def get_director_movies(id):
    director = Director.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Director.to_collection_dict(director.directed, page, per_page, 'api.get_director_movies', id=id) #TODO:Change endpoint
    return jsonify(data)


@bp.route('/directors', methods=['POST'])
@token_auth.login_required
def create_director():
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
    response.headers['Location'] = url_for('api.get_director', id=director.director_id)
    db.session.commit()
    return response


@bp.route('/directors/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_director(id):
    director = Director.query.get_or_404(id)
    data = request.get_json() or {}
    if 'f_name' in data and 'l_name' in data and\
            data['f_name'] != director.f_name and data['l_name'] != director.l_name and\
            Director.query.filter_by(f_name=data['f_name'], l_name=data['l_name']).first():
        return bad_request('Please use a different username')
    director.from_dict(data)
    db.session.commit()
    return jsonify(director.to_dict())


@bp.route('/directors/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_director(id):
    director = Director.query.get_or_404(id)
    db.session.delete(director)
    db.session.commit()
    return jsonify(director.to_dict())
