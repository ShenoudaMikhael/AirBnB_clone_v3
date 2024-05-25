#!/usr/bin/python3
"""create a file index_.py"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """get status"""
    return jsonify({"status": "OK"})
