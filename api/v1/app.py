#!/usr/bin/python3
"""
starts a Flask web application
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """Not Found Handler"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    """Closes connection"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))  # convert str to int
    app.run(host=host, port=port, threaded=True)
