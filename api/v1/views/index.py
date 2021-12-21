#!/usr/bin/python3
"""returns status"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def json_status():
    """returns status in JSON"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def status():
    """counts each model"""
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
