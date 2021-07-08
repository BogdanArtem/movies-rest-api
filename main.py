from app import app
from app.models import User, Genre, Director, Movie
from app import db


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': User, 'director': Director, 'genre': Genre, 'movie': Movie}


if __name__ == '__main__':
    app.run(debug=True)
