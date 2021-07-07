"""Flask representation of models in database"""


from app import db


genre_movie = db.Table('genre_movie',
                       db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id')),
                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'))
                       )


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    pass_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship('Movie', backref='user_added', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.f_name}, {self.l_name}>'


class Director(db.Model):
    director_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    directed = db.relationship('Movie', backref='directed_by', lazy='dynamic')

    def __repr__(self):
        return f'<Director {self.f_name}, {self.l_name}>'


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Genre {self.genre_id}, {self.name}>'


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id', ondelete='SET NULL'))
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)

    check = db.CheckConstraint('rating <= 10 AND rating >= 0')

    def __repr__(self):
        return f'<Director {self.f_name}, {self.l_name}>'
