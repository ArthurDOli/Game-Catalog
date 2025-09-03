from gamecatalog import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_usuario(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=False, default='default.jpg')
    logs = db.relationship('UserGameLog', backref='user', lazy=True, cascade="all, delete-orphan")

class UserGameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    game_slug = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    review_title = db.Column(db.String, nullable=True)
    review_text = db.Column(db.Text, nullable=True)