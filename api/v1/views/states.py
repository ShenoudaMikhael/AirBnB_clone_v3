#!/usr/bin/python3
"""create a file states.py"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, abort
from flask import jsonify


@app_views.route("/states/<id>")
@app_views.route("/states", defaults={"id": None})
def get_states(id):
    """get all states"""
    if id:
        if storage.get(State, id):
            return jsonify(storage.get(State, id).to_dict())
        abort(404)
    return jsonify([s.to_dict() for s in storage.all(State).values()])


@app_views.route("/states", methods=["post"])
def post_states():
    """post state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    a = State(**data)
    storage.new(a)
    storage.save()
    return jsonify(a.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["delete"])
def delete_state(state_id):
    """delete all states"""
    if state_id:
        st = storage.get(State, state_id)
        if st:
            storage.delete(st)
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    state.name = data.get("name")

    storage.save()
    return jsonify(state.to_dict()), 200
