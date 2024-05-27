#!/usr/bin/python3
"""index file"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    status route
    :return: response with json
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stat():
    """
    retrieves number of each object type
    Return: return response with json
    """
    data = {
        "amenities": str(storage.count("Amenity")),
        "cities": str(storage.count("City")),
        "places": str(storage.count("Place")),
        "reviews": str(storage.count("Review")),
        "states": str(storage.count("State")),
        "users": str(storage.count("User"))
    }
    return jsonify(data)
