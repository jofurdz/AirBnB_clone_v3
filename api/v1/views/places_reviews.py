#!/usr/bin/python3
"""new view for review"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<places_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def place_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    res = []
    for review in place.reviews:
        res.append(review.to_dict())
    return jsonify(res)

@app_views.route('/reviews/<review_id>', methods=['PUT', 'DELETE'],
                 strict_slashes=False)
def get_review(review_id):
    """updates review object"""
    if request.method == 'PUT':
        review_info = storage.get(Review, review_id)
        ignore_keys = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
        if review_info is not None:
            if not request.is_json:
                return "Not a JSON", 400

        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(review_info, key, value)
        storage.save()
        return jsonify(review_info.to_dict()), 200
    abort(404)

    if request.method == 'DELETE':
        review_info = storage.get(Review, review_id)
        if review_info is None:
            abort(404)
        else:
            storage.delete(review_info)
            storage.save()
            return jsonify({}), 200

@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    review_info = request.get_json()
    if not place:
        abort(404)
    elif not review_info:
        abort(400, "Not a JSON")
    elif "name" not in review_info.keys():
        abort(400, "Missing name")
    if "text" not in review_info.keys():
        abort(400, "Missing text")
    user_id = review_info.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    elif storage.get("User", user_id) is None:
        abort(404)
    else:
        review = Review(**review_info)
        review.place_id = place_id
        storage.new(review)
        storage.save()
        return jsonify(place.to_dict()), 201
