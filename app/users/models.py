from app import db, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default="default.png")
    about_me = db.Column(db.String(140), nullable=True)
    last_seen = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"User ('{self.email}')"
    
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)