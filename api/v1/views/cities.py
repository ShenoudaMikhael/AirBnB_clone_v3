#!/usr/bin/python3
"""create a file cities.py"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import request, abort, jsonify


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """get all cities of state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Retrieve City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Delete City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Create City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    if "name" not in data:
        abort(400, jsonify({"error": "Missing name"}))
    data["state_id"] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, {"error": "Not a JSON"})
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
