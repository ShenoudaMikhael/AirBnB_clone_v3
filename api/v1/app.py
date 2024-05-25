#!/usr/bin/python3
"""
starts a Flask web application
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """Not Found Handler"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def close_storage(exception):
    """Closes connection"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))  # convert str to int
    app.run(host=host, port=port, threaded=True)
