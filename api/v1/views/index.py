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

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
    # return {k: storage.count(v) for k, v in classes.items()}
