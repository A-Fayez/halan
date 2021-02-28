from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


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
        return make_response(jsonify({"ip": request.remote_addr}), 200)


api.add_resource(HalanRocks, "/")
api.add_resource(IpResource, "/ip")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
