#!/usr/bin/python3
"""create routes for places_reviews.py"""
from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    """Retrieve the list of all reviews of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([pl.to_dict() for pl in place.reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Retrieve the list of all Place objects of a City"""
    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a review object"""

    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)
    storage.delete(rev)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Delete a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    if "text" not in data:
        abort(400, jsonify({"error": "Missing text"}))

    if "user_id" not in data:
        abort(400, jsonify({"error": "Missing user_id"}))

    if storage.get(User, data.get("user_id")) is None:
        abort(404)

    rev = Review(place_id=place_id, **data)
    storage.new(rev)
    storage.save()
    return jsonify(rev.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_rev(review_id):
    """Update an review object"""
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, jsonify({"error": "Not a JSON"}))
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id" "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
