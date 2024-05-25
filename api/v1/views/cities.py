#!/usr/bin/python3
"""create a file cities.py"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, abort


@app_views.route("/states/<state_id>/cities")
def get_cities(state_id):
    """get all cities of state"""
    # Start hereee  Bellaaaaaaaaaaaa
    if state_id:
        if storage.get(State, id):
            return storage.get(State, id).cities
        abort(404)
    return {}
