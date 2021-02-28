from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

import os

app = Flask(__name__)
api = Api(app)
app.config.from_object("config.Config")
db = SQLAlchemy(app)
db.create_all()

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("No database configurateion detected")


class HalanRocks(Resource):
    def get(self):
        n = request.args.get("n")
        if n:
            try:
                n = int(n)
            except:
                return "Invalid Number", 400
            return n * n

        return "Halan ROCKS"


class IpResource(Resource):
    def get(self):
        ip = request.remote_addr
        db.session.add(Ip(ip_str=ip))
        db.session.commit()
        return make_response(jsonify({"ip": ip}), 200)


class AllIpResource(Resource):
    def get(self):
        ips = Ip.query.all()
        return make_response(jsonify({"ips": ips}), 200)


api.add_resource(HalanRocks, "/")
api.add_resource(IpResource, "/ip")
api.add_resource(AllIpResource, "/allips")


@dataclass
class Ip(db.Model):
    __tablename__ = "ips"

    id: int
    ip_str: str

    id = db.Column(db.Integer, primary_key=True)
    ip_str = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"ip: {self.ip_str}"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
