"""Users endpoint"""


from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import error_response
from app.models import User
from app.api.auth import token_auth


@bp.route('/users/<int:item_id>', methods=['GET'])
@token_auth.login_required
def get_user(item_id):
    """Get user by id or 404"""
    user = User.query.get_or_404(item_id)
    current_user = token_auth.current_user()
    # Allow user to read it's own data
    if current_user.is_admin or current_user.id == user.id:
        return jsonify(user.to_dict())
    return error_response(403, "User requesting this data does not have right permissions")


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """Get all users in paginated format"""
    current_user = token_auth.current_user()
    if current_user.is_admin:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
        return jsonify(data)
    return error_response(403, "User requesting this data does not have right permissions")


@bp.route('/users/<int:item_id>/movies', methods=['GET'])
@token_auth.login_required
def get_user_movies(item_id):
    """Get all movies related to user"""
    user = User.query.get_or_404(item_id)
    current_user = token_auth.current_user()
    if current_user.is_admin or user.id == current_user.id:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        data = User.to_collection_dict(user.movies, page, per_page,
                                       'api.get_user_movies', item_id=item_id)
        return jsonify(data)
    return error_response(403, "User requesting this data does not have right permissions")


@bp.route('/users', methods=['POST'])
def create_user():
    """Add new user with post request"""
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return error_response(400, 'Must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return error_response(409, 'Please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return error_response(409, 'Please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', item_id=user.id)
    return response


@bp.route('/users/<int:item_id>', methods=['PUT'])
@token_auth.login_required
def update_user(item_id):
    """Change any parameter of user or 404"""

    user = User.query.get_or_404(item_id)
    current_user = token_auth.current_user()

    data = request.get_json() or {}
    # Data validation
    if 'name' in data and data['name'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return error_response(409, 'Please use a different username')
    # Only users can change its data (or admins)
    if user.id == current_user.id:
        if 'is_admin' in data and data['is_admin'] is True:
            return error_response(403, 'You are not allowed to modify admin attribute')
        user.from_dict(data, new_user=False)
        db.session.commit()
        return jsonify(user.to_dict())
    # Admins can create new admins
    if current_user.is_admin:
        user.from_dict(data, is_admin=True)
        db.session.commit()
        return jsonify(user.to_dict())
    return error_response(403, "User changing this data does not have right permissions")


@bp.route('/users/<int:item_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(item_id):
    """Delete user or 404"""
    user = User.query.get_or_404(item_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.to_dict())
