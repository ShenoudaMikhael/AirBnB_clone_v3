#!/usr/bin/python3
"""create routes for states"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, abort
from flask import jsonify


@app_views.route("/states/<state_id>")
@app_views.route("/states", defaults={"state_id": None})
def get_states(state_id):
    """get all states"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            return abort(404)
        return jsonify(state.to_dict())
    return jsonify([s.to_dict() for s in storage.all(State).values()])


@app_views.route("/states", methods=["post"])
def post_states():
    """post state"""
    data = {}
    try:
        data = request.get_json()
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    if "name" not in data:
        abort(400, jsonify({"error": "Missing name"}))
    a = State(**data)
    storage.new(a)
    storage.save()
    return jsonify(a.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["DELETE"])
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
    try:
        data = request.get_json()
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
