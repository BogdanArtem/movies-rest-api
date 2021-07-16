from app import app
from app.models import User, Genre, Director, Movie
from app import db
from app import cli


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Director': Director, 'Genre': Genre, 'Movie': Movie}

if __name__ == '__main__':
    app.run()
