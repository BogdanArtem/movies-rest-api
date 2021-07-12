"""Flask representation of models in database"""


from werkzeug.security import check_password_hash, generate_password_hash
from flask import url_for
from app import db


class PaginatedAPIMixin:
    """Class for generating api links with pagination for set of items """
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


genre_movie = db.Table('genre_movie',
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id')),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'))
                       )


class User(PaginatedAPIMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    pass_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship('Movie', backref='user_added', lazy='dynamic')

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def to_dict(self):
        data = {
            'id': self.user_id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            #'password': self.pass_hash,
            'movies_count': self.movies.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.user_id),
                'movies': url_for('api.get_user_movies', id=self.user_id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    def __repr__(self):
        return f'<User {self.username}, {self.email}>'


class Director(PaginatedAPIMixin, db.Model):
    director_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    directed = db.relationship('Movie', backref='directed_by', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.director_id,
            'name': self.f_name,
            'surname': self.l_name,
            'movies_count': self.directed.count(),
            '_links': {
                'self': url_for('api.get_director', id=self.director_id),
                'movies': url_for('api.get_director_movies', id=self.director_id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['f_name', 'l_name']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Director {self.f_name}, {self.l_name}>'


class Genre(PaginatedAPIMixin, db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', secondary=genre_movie,
                             # primary_join=(genre_movie.c.genre_id == genre_id),
                             # secondary_join=(genre_movie.c.movie_id == genre_id),
                             backref=db.backref('genres', lazy='dynamic'), lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.genre_id,
            'name': self.name,
        }
        return data

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Genre {self.name}>'


class Movie(PaginatedAPIMixin, db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id', ondelete='SET NULL'))
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)

    check = db.CheckConstraint('rating <= 10 AND rating >= 0')

    def to_dict(self):
        data = {
            'id': self.movie_id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'rating': self.rating,
            'user': self.user_id,
            '_links': {
                'self': url_for('api.get_director', id=self.director_id),
                'user': url_for('api.get_director_movies', id=self.director_id),
                'director': url_for('api.get_director_movies', id=self.director_id),
                # 'genres'
                'poster_url': self.poster_url
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'date', 'description', 'rating', 'user', 'director_id', 'user_id', 'poster_url']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Movie {self.name}>'
