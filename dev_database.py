from app import db
from app.models import User, Genre, Movie, Director
from werkzeug.security import generate_password_hash


usr1 = User(username='Alex', email='timsmith@gmail.com', is_admin=True, pass_hash=generate_password_hash('12345'))
usr2 = User(username='Gim', email='Gim@gmail.com', is_admin=False, pass_hash=generate_password_hash('12345'))
usr3 = User(username='Donald', email='Donald@gmail.com', is_admin=False, pass_hash=generate_password_hash('12345'))

db.session.add(usr1)
db.session.add(usr2)
db.session.add(usr3)

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

mov1 = Movie(name='Good movie', director_id=2, date='1995-01-01',
             description='One of the best movies I have ever seen',
             rating=6, poster_url='www.valera.com', user_id=2)

mov2 = Movie(name='Nice movie', director_id=2, date='1993-01-01',
             description='I do not regret going to this movie',
             rating=6, poster_url='www.valera.com', user_id=2)

mov3 = Movie(name='Super movie', director_id=1, date='1992-01-01',
             description='Simply the best',
             rating=6, poster_url='www.valera.com', user_id=2)


db.session.add(mov1)
db.session.add(mov2)
db.session.add(mov3)

db.session.commit()

# Elasticsearch indexing
Movie.reindex()
