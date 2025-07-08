from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider
from route.route import route_bp

import json
import sys

app = Flask(__name__)

app.register_blueprint(route_bp)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
