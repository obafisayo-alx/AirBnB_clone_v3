#!/usr/bin/python3
"""A view for State Objects"""


from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states():
    """Handles GET and POST requests for /states route.
    Return: a state object or a list of states
    """
    if request.method == 'GET':
        states_list = [state.to_dict()
                       for state in storage.all(State).values()]
        return jsonify(states_list)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(404, description="Not a JSON")
        if 'name' not in data:
            abort(404, description="Missing name")
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def state_by_id(state_id):
    """Handles GET, PUT and DELETE request for /states/<state_id>

    Keyword arguments:
    state_id -- this is the state id
    Return: returns the individual state gotten by the id or error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(404, description="Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
