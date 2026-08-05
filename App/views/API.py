from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers.user import get_all_users_json,create_user

api_views = Blueprint('api_views',__name__, url_prefix='/api')

@api_views.route('/ping',methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

'User API Endpoints'
@api_views.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = get_all_users_json()
    return jsonify(users), 200

@api_views.route('/create_user',methods=['POST'])
@jwt_required()
def create_general_user():
    data = request.json
    user = create_user(data['username'],data['password'],data['is_admin'])
    if user:
        return jsonify({"message":f"User created!"}),201
    return jsonify({"message":f"User could not be created!"}),400

