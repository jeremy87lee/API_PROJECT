from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, set_access_cookies
from App.controllers.user import get_all_users_json,create_user,get_all_flights_json,create_Flight,get_all_users,update_flight,delete_flight
from App.controllers.user import get_all_planes_json
from App.controllers import login,initialize
from App.models.Flights import Flight

api_views = Blueprint('api_views',__name__, url_prefix='/api')

@api_views.route('/ping',methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

@api_views.route('/login',methods=['POST'])
def login_function():
    data = request.json
    token = login(data.get("username"),data.get("password"))
    if token:
        response = jsonify(access_token=token)
        set_access_cookies(response, token)
        return response
    else:
        return jsonify({"message":f"Bad Credentials!"}),401

@api_views.route('/init',methods=['GET'])
def init():
    initialize()
    return jsonify("Database Initialized!"),200

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
        return jsonify({"message":f"Missing credentials!"}),400
    users = get_all_users()
    for u in users:
        if u.username == data.get("username"):
            return jsonify({"message":f"Username already taken!"}),409
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
    if not jwt_current_user.is_admin:
        return jsonify({"message" : f"Only admins can create flights!"}),401
    data = request.json
    if data.get("departure_time") is None or data.get("arrival_time") is None or data.get("plane_id") is None or data.get("pilot_id") is None or data.get("departure_destination") is None or data.get("arrival_destination") is None:
        return jsonify({"message" : f"Missing flight data! Could not be created!"}),400
    new_flight = create_Flight(data.get("departure_time"),data.get("arrival_time"),data.get("plane_id"),data.get("pilot_id"),data.get("departure_destination"),data.get("arrival_destination"))
    if new_flight:
        return jsonify({"message":f"Flight created!"}),201
    return jsonify({"message":f"Flight could not be created!"}),404

@api_views.route('/update_flight/<int:flight_id>',methods=['PUT'])
@jwt_required()
def update_flight_function(flight_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message" : f"Only admins can update flights!"}),401
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message":f"Flight not found!"}),404
    data = request.json
    if data.get("departure_time") is None or data.get("arrival_time") is None or data.get("plane_id") is None or data.get("pilot_id") is None or data.get("departure_destination") is None or data.get("destination") is None:
        return jsonify({"message":f"Missing flight data! Could not update!"}),400
    update = update_flight(data.get("departure_time"),data.get("arrival_time"),data.get("plane_id"),data.get("pilot_id"),data.get("departure_destination"),data.get("destination"),flight_id)
    if not update:
        return jsonify({"message":f"Flight could not be updated!"}),400
    return jsonify({"message":f"Flight updated!"}),200

@api_views.route('/delete_flight/<int:flight_id>',methods=['DELETE'])
@jwt_required()
def delete_flight_function(flight_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can delete flights!"}),401
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message":f"Flight number {flight_id} could not be found!"}),404
    deletion = delete_flight(flight_id)
    if not deletion:
        return jsonify({"message":f"Flight number {flight_id} could not be deleted!"}),400
    return jsonify({"message":f"Flight number {flight_id} deleted!"})

'Plane Endpoints'
@api_views.route('/planes',methods=['GET'])
@jwt_required()
def display_planes():
    planes = get_all_planes_json()
    return jsonify(planes),200