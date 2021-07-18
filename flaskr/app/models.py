"""Flask representation of models in database"""

import os
import base64
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask import url_for
from app import db
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin:
    """This class allows maintaining indexes for elasticsearch"""

    @classmethod
    def search(cls, expression, page, per_page):
        """Adds search in elasticsearch index from model"""
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """Save all the changes to be committed as attribute for use in after_commit"""
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        """Apply committed changes to elasticsearch"""
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Update elasticsearch index for model"""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class PaginatedAPIMixin:
    """Class for generating api links with pagination"""

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """Universal method to generate paginated response from any query"""
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
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) \
                    if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) \
                    if resources.has_prev else None
            }
        }
        return data


genre_movie = db.Table('genre_movie',
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
                       )


class User(PaginatedAPIMixin, db.Model):
    """User model with support of authentication and pagination"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(128), nullable=False, index=True, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    pass_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship('Movie', backref='user_added', lazy='dynamic')

    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        """Create hash of password and add it to model"""
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check stored hash against password hash"""
        return check_password_hash(self.pass_hash, password)

    def get_token(self, expires_in=86400):
        """Returns unexpired token from model or creates new one before returning"""
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """Makes token invalid"""
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """Check token validity"""
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        """Convert object to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            # 'password': self.pass_hash,
            'movies_count': self.movies.count(),
            '_links': {
                'self': url_for('api.get_user', item_id=self.id),
                'movies': url_for('api.get_user_movies', item_id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        """Create object from dictionary"""
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    def __repr__(self):
        return f'<User {self.username}, {self.email}>'


class Director(PaginatedAPIMixin, db.Model):
    """Director model with reference to movies"""
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    directed = db.relationship('Movie', backref='directed_by', lazy='dynamic')

    def to_dict(self):
        """Convert object to dictionary"""
        data = {
            'id': self.id,
            'name': self.f_name,
            'surname': self.l_name,
            'movies_count': self.directed.count(),
            '_links': {
                'self': url_for('api.get_director', item_id=self.id),
                'movies': url_for('api.get_director_movies', item_id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        """Convert dictionary to object"""
        for field in ['f_name', 'l_name']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Director {self.f_name}, {self.l_name}>'


class Genre(PaginatedAPIMixin, db.Model):
    """Genre model with movies relationship"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship('Movie', secondary=genre_movie,
                             # primary_join=(genre_movie.c.genre_id == genre_id),
                             # secondary_join=(genre_movie.c.movie_id == genre_id),
                             backref=db.backref('genres', lazy='dynamic'), lazy='dynamic')

    def to_dict(self):
        """Convert object to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
        }
        return data

    def from_dict(self, data):
        """Convert dictionary to object"""
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Genre {self.name}>'


class Movie(SearchableMixin, PaginatedAPIMixin, db.Model):
    """Movie model with searchable fields and constraints"""
    __searchable__ = ['name', 'description']
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id', ondelete='SET NULL'))
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    description = db.Column(db.Text, index=True)
    rating = db.Column(db.Integer, db.CheckConstraint('rating <= 10 AND rating >= 0'), nullable=False)
    poster_url = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Convert object to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'rating': self.rating,
            'user': self.user_id,
            '_links': {
                'director': 'unknown' if self.director_id is None else
                url_for('api.get_director', item_id=self.director_id),
                'user': 'unknown' if self.user_id is None else
                url_for('api.get_user', item_id=self.user_id),
                'poster_url': self.poster_url
            }
        }
        return data

    def from_dict(self, data):
        """Convert dictionary to object"""
        for field in ['name', 'date', 'description', 'rating',
                      'user', 'director_id', 'user_id', 'poster_url']:
            # Sqlite fix
            if field in data and field == 'date':
                date = datetime.strptime(data[field], '%Y-%m-%d')
                setattr(self, field, date)
            elif field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Movie {self.name}>'


db.event.listen(db.session, 'before_commit', Movie.before_commit)
db.event.listen(db.session, 'after_commit', Movie.after_commit)
