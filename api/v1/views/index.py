#!/usr/bin/python3
"""blueprint routes"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Display the status of the API"""
    return jsonify({"status": "OK"})
