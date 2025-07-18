#!/usr/bin/env python3
"""
class to manage the API authentication.
"""
from flask import request, jsonify
from models.user import User
from api.v1.views import app_views
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    if not password:
        return jsonify({ "error": "password missing" }), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({ "error": "no user found for this email" }), 404
    if not user[0].is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    resp = jsonify(user[0].to_json())
    resp.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return resp

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
