from app import app, db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Date
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.Float)
    sentiment_label = db.Column(db.String(10))
    date = db.Column(Date, default=datetime.utcnow().date()) 

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=True)

    @staticmethod
    def create_admin():
        existing_admin = User.query.filter_by(role='admin').first()
        if not existing_admin:
            admin = User(username='admin', password='admin_password', role='admin')
            db.session.add(admin)
            db.session.commit()
# Create the database tables
with app.app_context():
    db.create_all()
    User.create_admin()