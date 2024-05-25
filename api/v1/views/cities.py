#!/usr/bin/python3
"""create a file cities.py"""

from api.v1.views import app_views
from models import storage
from models.city import City
from flask import request, abort


@app_views.route("/states/<state_id>/cities")
def get_cities(state_id):
    """get all cities"""
    if state_id:
        if storage.get(City, id):
            return storage.get(City, id).to_dict()
        abort(404)
    return [s.to_dict() for s in storage.all(City).values()]


@app_views.route("/cities", methods=["post"])
def post_city():
    """post city"""
    data = request.get_json()
    a = City(**data)
    storage.new(a)
    storage.save()
    return a.to_dict(), 201


@app_views.route("/cities/<id>", methods=["delete"])
def delete_city(id):
    """delete all cities"""
    if id:
        st = storage.get(City, id)
        if st:
            storage.delete(st)
            storage.save()
            return {}, 200
        abort(404)
