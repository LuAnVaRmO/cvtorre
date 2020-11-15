#!/usr/bin/env python3
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
import requests

@app_views.route('/status', methods=['GET'])
def status():
    """ Return status 200 if ok """
    return jsonify({"status": "OK"})
