#!/usr/bin/python3
"""create a file index_.py"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


@app_views.route("/status")
def get_status():
    """get status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """get stats"""
    q = {}
    for c, v in classes.items():
        count = storage.count(v)
        q[c] = count
    return jsonify(q)
