from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, set_access_cookies
from App.controllers.user import get_all_users_json,create_user,get_all_flights_json,create_Flight,get_all_users
from App.controllers import login

api_views = Blueprint('api_views',__name__, url_prefix='/api')

@api_views.route('/ping',methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

@api_views.route('/login',methods=['POST'])
def login_function():
    data = request.json
    token = login(data.get("username"),data.get("password"))
    return jsonify({"message":f"Logged in!"}),200
    

'User API Endpoints'
@api_views.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = get_all_users_json()
    return jsonify(users), 200

@api_views.route('/create_user',methods=['POST'])
def create_general_user():
    data = request.json
    if data.get("username") is None or data.get("password") is None or data.get("is_admin") is None:
        return jsonify({"message":f"Missing credentials!"}),401
    users = get_all_users()
    for u in users:
        if u.username == data.get("username"):
            return jsonify({"message":f"Username already taken!"}),401
    user = create_user(data.get("username"),data.get("password"),data.get("is_admin"))
    if user:
        return jsonify({"message":f"User created!"}),201
    return jsonify({"message":f"User could not be created!"}),400

'Flight API endpoints'
@api_views.route('/flights',methods=['GET'])
@jwt_required()
def get_flights():
    flights = get_all_flights_json()
    return jsonify(flights),200

@api_views.route('/create_flight',methods=['POST'])
@jwt_required()
def create_flight_function():
    data = request.json
    if data.get("departure_time") is None or data.get("arrival_time") is None or data.get("plane_id") is None or data.get("pilot_id") is None or data.get("departure_destination") is None or data.get("arrival_destination") is None:
        return jsonify({"message" : f"Missing flight data! Could not be created!"}),400
    new_flight = create_Flight(data.get("departure_time"),data.get("arrival_time"),data.get("plane_id"),data.get("pilot_id"),data.get("departure_destination"),data.get("arrival_destination"))
    if new_flight:
        return jsonify({"message":f"Flight created!"}),201
    return jsonify({"message":f"Flight could not be created!"}),400