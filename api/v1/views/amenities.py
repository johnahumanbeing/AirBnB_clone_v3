from flask import Flask, jsonify, request, abort
from . import app_views
from models import Amenity

@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict() for amenity in Amenity.all()]
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = Amenity.get(amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
