from flask_sqlalchemy import SQLAlchemy
import datetime

from app.Controller.app import db  


class APILog(db.Model):
    __tablename__ = 'logs'
    id        = db.Column(db.Integer,   primary_key=True)
    username  = db.Column(db.String(80), nullable=False)
    endpoint  = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime,  default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, username, endpoint, timestamp=None):
        """
        Initialize a new APILog.

        :param username: the user (string)
        :param endpoint: the endpoint or path accessed (string)
        :param timestamp: optional datetime; defaults to utcnow()
        """
        self.username = username
        self.endpoint = endpoint
        # use provided timestamp or default to now
        self.timestamp = timestamp or datetime.datetime.now(datetime.timezone.utc)