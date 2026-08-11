from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, set_access_cookies
from App.controllers.user import get_all_users_json,create_user,get_all_flights_json,create_Flight,get_all_users,update_flight,delete_flight
from App.controllers.user import get_all_planes_json, create_Plane, update_plane, delete_plane
from App.controllers.user import get_all_pilots_json, create_Pilot, update_pilot, delete_pilot
from App.controllers.user import get_all_gates_json, create_Gate, update_gate, delete_gate
from App.controllers import login,initialize
from App.models.Flights import Flight,Plane,Pilot
from App.models.Gates import Gate

api_views = Blueprint('api_views',__name__, url_prefix='/api')

@api_views.route('/ping',methods=['GET'])
def ping():
    return jsonify({"message":f"pong"}), 200

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
    return jsonify({"message":f"Database Initialized!"}),200

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
    page = request.args.get("page",1,type=int)
    per_page = request.args.get("per_page",3,type=int)
    destination = request.args.get("destination",None)
    sort = request.args.get("sort",None)
    flights = get_all_flights_json(page=page,per_page=per_page,destination=destination,sort=sort)
    return jsonify(flights),200

@api_views.route('/create_flight',methods=['POST'])
@jwt_required()
def create_flight_function():
    if not jwt_current_user.is_admin:
        return jsonify({"message" : f"Only admins can create flights!"}),401
    data = request.json
    if not data.get("departure_time")  or not data.get("arrival_time") or not data.get("plane_id") or not data.get("pilot_id") or not data.get("departure_destination") or not data.get("arrival_destination"):
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
    if not data.get("departure_time") or not data.get("arrival_time") or not data.get("plane_id") or not data.get("pilot_id") or not data.get("departure_destination") or not data.get("destination"):
        return jsonify({"message":f"Missing flight data! Could not update!"}),400
    update = update_flight(data.get("departure_time"),data.get("arrival_time"),data.get("plane_id"),data.get("pilot_id"),data.get("departure_destination"),data.get("destination"),flight_id)
    if not update:
        return jsonify({"message":f"Flight could not be updated!"}),400
    return jsonify({"message":f"Flight {flight_id} updated!"}),200

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
    return jsonify({"message":f"Flight number {flight_id} deleted!"}),200

'Plane Endpoints'
@api_views.route('/planes',methods=['GET'])
@jwt_required()
def display_planes():
    page = request.args.get("page",type=int)
    per_page = request.args.get("per_page",type=int)
    model = request.args.get("model",None)
    sort = request.args.get("sort",None)
    planes = get_all_planes_json(page=page,per_page=per_page,model=model,sort=sort)
    return jsonify(planes),200

@api_views.route('/create_plane',methods=['POST'])
@jwt_required()
def create_plane_function():
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can create planes!"}),401
    data = request.json
    if not data.get("model") or not data.get("capacity"):
        return jsonify({"message":f"Model or Capacity info missing!"}),400
    new_plane = create_Plane(data.get("model"),data.get("capacity"))
    if not new_plane:
        return jsonify({"message":f"Plane could not be created!"}),400
    return jsonify({"message":f"Plane created!"}),201

@api_views.route('/update_plane/<int:plane_id>',methods=['PUT'])
@jwt_required()
def update_plane_function(plane_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can update planes!"}),401
    plane = Plane.query.get(plane_id)
    if not plane:
        return jsonify({"message":f"Plane number {plane_id} not found!"}),404
    data = request.json
    if not data.get("model") or not data.get("capacity"):
        return jsonify({"message":f"Model or Capacity info missing!"}),400
    new_plane = update_plane(plane_id,data.get("model"),data.get("capacity"))
    if not new_plane:
        return jsonify({"message":f"Plane could not be updated!"}),400
    return jsonify({"message":f"Plane {plane_id} updated!"}),200

@api_views.route('/delete_plane/<int:plane_id>',methods=['DELETE'])
@jwt_required()
def delete_plane_function(plane_id):
    if not jwt_current_user.is_admin:
            return jsonify({"message":f"Only admins can delete planes!"}),401
    plane = Plane.query.get(plane_id)
    if not plane:
        return jsonify({"message":f"Plane number {plane_id} not found!"}),404
    deletion = delete_plane(plane_id)
    if not deletion:
        return jsonify({"message":f"Plane number {plane_id} not deleted!"}),400
    return jsonify({"message":f"Plane {plane_id} deleted!"}),200

'Pilot Endpoints'
@api_views.route('/pilots',methods=['GET'])
@jwt_required()
def display_pilots():
    page = request.args.get("page",type=int)
    per_page = request.args.get("per_page",type=int)
    sort = request.args.get("sort",None)
    pilots = get_all_pilots_json(page=page,per_page=per_page,sort=sort)
    return jsonify(pilots)

@api_views.route('/create_pilot',methods=['POST'])
@jwt_required()
def create_pilot_function():
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can create pilots!"}),401
    data = request.json
    if not data.get("name"):
        return jsonify({"message":f"Name not given!"}),400
    new_pilot = create_Pilot(data.get("name"))
    if not new_pilot:
        return jsonify({"message":f"Pilot could not be created!"}),400
    return jsonify({"message":f"Pilot created!"}),201

@api_views.route('/update_pilot/<int:pilot_id>',methods=['PUT'])
@jwt_required()
def update_pilot_function(pilot_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can update pilots!"}),401
    pilot = Pilot.query.get(pilot_id)
    if not pilot:
        return jsonify({"message":f"Pilot number {pilot_id} not found!"}),404
    data = request.json
    if not data.get("name"):
        return jsonify({"message":f"Name info missing!"}),400
    new_pilot = update_pilot(pilot_id,data.get("name"))
    if not new_pilot:
        return jsonify({"message":f"Pilot could not be updated!"}),400
    return jsonify({"message":f"Pilot {pilot_id} updated!"}),201

@api_views.route('/delete_pilot/<int:pilot_id>',methods=['DELETE'])
@jwt_required()
def delete_pilot_function(pilot_id):
    if not jwt_current_user.is_admin:
            return jsonify({"message":f"Only admins can delete pilots!"}),401
    pilot = Pilot.query.get(pilot_id)
    if not pilot:
        return jsonify({"message":f"Pilot number {pilot_id} not found!"}),404
    deletion = delete_pilot(pilot_id)
    if not deletion:
        return jsonify({"message":f"Pilot number {pilot_id} not deleted!"}),400
    return jsonify({"message":f"Pilot {pilot_id} deleted!"}),200

'Gate Endpoints'
@api_views.route('/gates',methods=['GET'])
@jwt_required()
def display_gates():
    gates = get_all_gates_json()
    return jsonify(gates)

@api_views.route('/create_gate',methods=['POST'])
@jwt_required()
def create_gate_function():
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can create gates!"}),401
    data = request.json
    if not data.get("terminal") or not data.get("flight_id"):
        return jsonify({"message":f"Missing terminal or flight id!"}),400
    new_gate = create_Gate(data.get("terminal"),data.get("flight_id"))
    if not new_gate:
        return jsonify({"message":f"Gate could not be created!"}),400
    return jsonify({"message":f"Gate created!"}),201

@api_views.route('/update_gate/<int:gate_id>',methods=['PUT'])
@jwt_required()
def update_gate_function(gate_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can create gates!"}),401
    data = request.json
    if not data.get("terminal") or not data.get("flight_id"):
        return jsonify({"message":f"Missing terminal or flight id!"}),400
    update = update_gate(gate_id,data.get("terminal"),data.get("flight_id"))
    if not update:
        return jsonify({"message":f"Gate {gate_id} could not be updated!"}),400
    return jsonify({"message":f"Gate {gate_id} updated!"}),200

@api_views.route('/delete_gate/<int:gate_id>',methods=['DELETE'])
@jwt_required()
def delete_gate_function(gate_id):
    if not jwt_current_user.is_admin:
        return jsonify({"message":f"Only admins can create gates!"}),401
    gate = Gate.query.get(gate_id)
    if not gate:
        return jsonify({"message":f"Gate {gate_id} not found!"}),404
    deletion = delete_gate(gate_id)
    if not deletion:
        return jsonify({"message":f"Gate {gate_id} could not be deleted!"}),400
    return jsonify({"message":f"Gate {gate_id} deleted!"}),200