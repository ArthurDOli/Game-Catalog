from gamecatalog import app, db
from gamecatalog.models import User, Review, UserGameStatus

with app.app_context():
    db.create_all()