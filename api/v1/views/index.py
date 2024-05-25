#!/usr/bin/python3
"""create a file index_.py"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """get status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """get stats"""
    # add storage.count after merge
    return jsonify({})
    # return jsonify(storage.count)
