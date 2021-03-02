from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import os

if not os.getenv("POSTGRESQL_PASSWORD"):
    raise RuntimeError("Error: POSTGRESQL_PASSWORD is not set")
_db_user = os.getenv("DB_USER", default="postgres")
_db_host = os.getenv("DB_HOST", default="pg-release-postgresql")
_db_port = os.getenv("DB_PORT", default="5432")
_db_name = os.getenv("DB_NAME", default="postgres")
_db_password = os.getenv("POSTGRESQL_PASSWORD")
_db_url = f"postgres://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"


class Config(object):

    SQLALCHEMY_DATABASE_URI = _db_url
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
