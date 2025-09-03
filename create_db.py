from gamecatalog import app, db
from gamecatalog.models import User, UserGameLog

with app.app_context():
    db.create_all()