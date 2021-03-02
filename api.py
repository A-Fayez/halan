from flask_restful import Api, Resource
from flask import make_response, jsonify, request
from config import db, Ip, app
import os

api = Api(app)
db.create_all()

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("No database configurateion detected")


class HalanRocks(Resource):
    def get(self):

        ip = request.remote_addr
        db.session.add(Ip(ip_str=ip))
        db.session.commit()

        n = request.args.get("n")
        if n:
            try:
                n = int(n)
            except ValueError:
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
