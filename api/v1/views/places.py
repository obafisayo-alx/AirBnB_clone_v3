#!/usr/bin/python3
"""A view for the places objects"""


from api.v1.views import app_views, storage
from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_belonging_to_city_id(city_id):
    """list of all place objects of a city

    Keyword arguments:
    city_id -- The id of the city whoose places is to be found
    Return: the list of places blonging to city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        if 'user_id' not in data:
            abort(400, description="Missing user_id")
        user_id = data.get('user_id')
        if not storage.get(User, user_id):
            abort(404)
        if 'name' not in data:
            abort(400, description="Missing name")
        place = Place(**data)
        place.user_id = user_id
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def places_by_id(place_id):
    """carrys out GET, PUT and DELETE requests on the returned place

    Keyword arguments:
    place_id -- the id of the place
    Return: returns the json representation of the object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, description="Not a JSON")

        data = request.get_json()
        if not data:
            abort(400, description="Not a JSON")
        for key, val in data.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, val)
        place.save()
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
