from app.api import bp


@bp.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    """Return one movie by id"""
    pass


@bp.route('/movies', methods=['GET'])
def get_movies():
    """Return all movies"""
    pass


@bp.route('/movies', methods=['POST'])
def create_movie():
    """Add movie"""
    pass


@bp.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    """Update movie by id"""
    pass
