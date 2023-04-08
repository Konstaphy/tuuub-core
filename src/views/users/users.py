from flask import Blueprint, jsonify

user_bp = Blueprint('users', __name__)


@user_bp.route('/login')
def login():
    # login view logic
    return jsonify({'message': 'login'})


@user_bp.route('/register')
def register():
    # register view logic
    return jsonify({'message': 'register'})
