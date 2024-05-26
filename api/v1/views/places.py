#!/usr/bin/python3
"""create routes for places"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import request, abort, jsonify


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_city_places(city_id):
    """Retrieve the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a Place object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    if "user_id" not in data:
        abort(400, jsonify({"error": "Missing user_id"}))
    if "name" not in data:
        abort(400, jsonify({"error": "Missing name"}))
    user_id = data["user_id"]
    if storage.get(User, user_id) is None:
        abort(404)
    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a Place object"""
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
