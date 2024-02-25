#!/usr/bin/python3
"""
View for City objects that handles
all default RESTful API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities_by_state(state_id):
    """Method to get all cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Method to get city by using id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Method to delete city by using id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Method to create a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    city = City(state_id=state_id, **data)
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Method to update a city by using id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ["id", "state_id", "created_at", "updated_at"]:
            continue
        setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
