from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///magic.db')
app = Flask(__name__)
api = Api(app)

class Fortunes(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select fortune from fortunes order by random() limit 1")
        return query.cursor.fetchall()

class Fortunes_Name(Resource):
    def get(self, fortune_id):
        conn = db_connect.connect()
        query = conn.execute("select fortune from fortunes where id = %d;"  %int(fortune_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(Fortunes, '/fortunes')
api.add_resource(Fortunes_Name, '/fortunes/<fortune_id>')


if __name__ == '__main__':
     app.run(port='5002')
