#!/usr/bin/python3
"""A view for cities objects"""


from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """Handles GET and POST requests for cities
    Keyword arguments:
    state_id -- the id of the state whoose city needs to be retrieved
    Return: returns the city for that state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = [city.to_dict()
                  for city in state.cities]
        return jsonify(cities)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        if 'name' not in data:
            abort(400, "Missing name")
        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201
