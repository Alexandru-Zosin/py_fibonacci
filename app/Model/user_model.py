from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username: str):
        # Note: SQLAlchemy will still handle the Column assignments for you
        self.username = username

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, username: str, password: str):
        """
        Look up by username, verify password, and return the user or None.
        """
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
