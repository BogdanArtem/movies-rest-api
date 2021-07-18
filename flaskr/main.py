from app import create_app, db, cli
from app.models import User, Genre, Director, Movie
app = create_app('development')
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Director': Director, 'Genre': Genre, 'Movie': Movie}
