#!/usr/bin/python3
"""
Route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    Retrieves all Place objects by city
    :return: JSON of all Places
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    place_list = [place.to_dict() for place in city_obj.places]
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    Gets a specific Place object by ID
    :param place_id: Place object ID
    :return: Place object with the specified ID or error
    """
    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Deletes Place by ID
    :param place_id: Place object ID
    :return: Empty dictionary with 200 or 404 if not found
    """
    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    Create place route
    :return: Newly created Place obj
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if not storage.get(User, place_json["user_id"]):
        abort(404)
    if "name" not in place_json:
        abort(400, 'Missing name')

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    Updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_dict())


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Search for places based on JSON request
    :return: JSON of matching Places
    """
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    if not data or all(not data[key] for key in ["states", "cities", "amenities"]):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places]), 200

    states = [storage.get(State, state_id) for state_id in data.get("states", [])]
    cities = [storage.get(City, city_id) for city_id in data.get("cities", [])]
    amenities = [storage.get(Amenity, amenity_id) for amenity_id in data.get("amenities", [])]

    if not states and not cities and not amenities:
        abort(400, "Invalid search criteria")

    places = []

    for state in states:
        places.extend(state.places)

    for city in cities:
        if city not in places:
            places.extend(city.places)

    if amenities:
        places = [place for place in places if all(amenity in place.amenities for amenity in amenities)]

    return jsonify([place.to_dict() for place in places]), 200
