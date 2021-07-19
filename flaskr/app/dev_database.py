"""Database initialization for testing"""


from datetime import date
from app.models import User, Director, Movie, Genre
from werkzeug.security import generate_password_hash
from app import db


def init_db():
    db.create_all()

    usr1 = User(username='Alex', email='timsmith@gmail.com',
                is_admin=False, pass_hash=generate_password_hash('12345'))
    usr2 = User(username='Gim', email='Gim@gmail.com',
                is_admin=False, pass_hash=generate_password_hash('12345'))
    usr3 = User(username='Donald', email='Donald@gmail.com',
                is_admin=False, pass_hash=generate_password_hash('12345'))
    usr4 = User(username='Admin', email='admind@gmail.com',
                is_admin=True, pass_hash=generate_password_hash('12345'))

    db.session.add(usr1)
    db.session.add(usr2)
    db.session.add(usr3)
    db.session.add(usr4)

    db.session.commit()

    dir1 = Director(f_name='Stiven', l_name='Spilberg')
    dir2 = Director(f_name='Nick', l_name='Stroter')
    dir3 = Director(f_name='Andrew', l_name='Bright')

    db.session.add(dir1)
    db.session.add(dir2)
    db.session.add(dir3)

    db.session.commit()

    gen1 = Genre(name='Romantic')
    gen2 = Genre(name='Sci-fi')
    gen3 = Genre(name='Action')

    db.session.add(gen1)
    db.session.add(gen2)
    db.session.add(gen3)

    db.session.commit()

    mov1 = Movie(name='Good movie', director_id=2, date=date(1993, 3, 19),
                 description='One of the best movies I have ever seen',
                 rating=5, poster_url='www.valera.com', user_id=2)

    mov2 = Movie(name='Nice movie', director_id=2, date=date(1995, 1, 9),
                 description='I do not regret going to this movie',
                 rating=6, poster_url='www.valera.com', user_id=2)

    mov3 = Movie(name='Super movie', director_id=1, date=date(1997, 3, 1),
                 description='Simply the best',
                 rating=7, poster_url='www.valera.com', user_id=2)

    mov4 = Movie(name='Last fight', director_id=1, date=date(1993, 3, 1),
                 description='Great fight of 2 armies',
                 rating=2, poster_url='www.valera.com', user_id=2)

    mov1.add_genre(gen1)
    mov1.add_genre(gen2)
    mov2.add_genre(gen1)
    mov3.add_genre(gen2)
    mov4.add_genre(gen3)

    db.session.add(mov1)
    db.session.add(mov2)
    db.session.add(mov3)
    db.session.add(mov4)

    db.session.commit()
