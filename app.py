from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

from models.main_model import MainModel

app = Flask(__name__)

api = Api(app)
CORS(app)

api.add_resource(MainModel, '/get-path')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
