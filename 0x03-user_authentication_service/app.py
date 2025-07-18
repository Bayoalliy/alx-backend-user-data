#!/usr/bin/env python3
"""
A Basic flask app
"""
from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def root_request():
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        try:
            new_user = AUTH.register_user(email, password)
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
        if new_user:
            return jsonify({'email': email, 'message': 'user created'})
    return jsonify({'message': 'email and/or password cant be empty'}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)
    
@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email})
    abort(403)

@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token})

@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('password')
    try:
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
