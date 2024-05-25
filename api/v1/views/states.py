#!/usr/bin/python3
"""create a file states.py"""

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states")
def get_states():
    """get all states"""
    return [s.to_dict() for s in storage.all(State)]
