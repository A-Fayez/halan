from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)


@dataclass
class Ip(db.Model):
    __tablename__ = "ips"

    id: int
    ip_str: str

    id = db.Column(db.Integer, primary_key=True)
    ip_str = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"ip: {self.ip_str}"

db.create_all()