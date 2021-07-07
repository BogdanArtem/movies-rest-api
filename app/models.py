"""Flask representation of models in database"""


from app import db


director_movie = db.Table('director_movie',
                          db.Column('director_id', db.Integer, db.ForeignKey('director.director_id')),
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.movie_id'))
                          )

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
    movies_directed = db.relationship('Movie', secondary=director_movie, backref='directors', lazy='dynamic')

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
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    # rating = db.Column(db.Enum(tuple(range(1, 11)), name='ratings'), nullable=False)
    poster_url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Director {self.f_name}, {self.l_name}>'
