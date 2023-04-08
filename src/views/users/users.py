from flask import Blueprint, jsonify
users_view = Blueprint('users', __name__)


@users_view.route('/login')
def login():
    # login view logic
    return jsonify({'message': 'login'})


@users_view.route('/register')
def register():
    # register view logic
    return jsonify({'message': 'register'})
