from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class APILog(db.Model):
    __tablename__ = 'logs'
    id        = db.Column(db.Integer,   primary_key=True)
    username  = db.Column(db.String(80), nullable=False)
    endpoint  = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime,  default=datetime.datetime.utcnow, nullable=False)
