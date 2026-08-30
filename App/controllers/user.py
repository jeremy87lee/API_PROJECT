from App.models import User
from App.database import db
from App.models.Gates import Gate
from App.models.Planes import Plane
from App.models.Admin import Admin
from App.models.Flights import Flight
from App.models.Pilots import Pilot
from datetime import datetime

def create_user(username, password, is_admin):
    if is_admin:
        newuser = create_admin(username, password, is_admin)
        return newuser
    else:
        newuser = User(username=username, password=password, is_admin=is_admin)
        db.session.add(newuser)
        db.session.commit()
        return newuser

def create_admin(username, password, is_admin):
    newadmin = Admin(username=username, password=password, is_admin=is_admin)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def create_Pilot(name):
    Pilots = Pilot.query.all()
    for pilot in Pilots:
        if pilot.name == name:
            print(f"Pilot with name {name} already exists.")
            return None  # Pilot already exists
    new_pilot = Pilot(name=name)
    db.session.add(new_pilot)
    db.session.commit()
    return new_pilot

def create_Plane(model, capacity):
    new_plane = Plane(model=model, capacity=capacity)
    db.session.add(new_plane)
    db.session.commit()
    return new_plane

def create_Gate(terminal, flight_id):
    flight_id = int(flight_id)
    flight = Flight.query.get(flight_id)
    if not flight:
        print(f"Flight ID {flight_id} does not exist.")
        return None  # Flight ID does not exist
    
    Flights = Gate.query.all()
    for f in Flights:
        if f.flight == flight_id:
            print(f"Gate for Flight ID {flight_id} already exists.")
            return None  # Gate for this flight already exists
    
    new_gate = Gate(terminal=terminal, flight=flight_id)
    db.session.add(new_gate)
    db.session.commit()
    return new_gate

def create_Flight(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination):
    plane_id = int(plane_id)
    pilot_id = int(pilot_id)
    plane = Plane.query.get(plane_id)
    if not plane:
        print(f"Plane ID {plane_id} does not exist.")
        return None  # Plane ID does not exist
    pilot = Pilot.query.get(pilot_id)
    if not pilot:
        print(f"Pilot ID {pilot_id} does not exist.")
        return None  # Pilot ID does not exist

    if departure_time >= arrival_time:
        print("Departure time must be before arrival time.")
        return None  # Invalid time range
    
    Flights = Flight.query.all()
    for f in Flights:
       
        if (departure_time < f.arrival_time and arrival_time > f.departure_time) and pilot_id == f.pilot_id:
            print(f"Pilot {pilot_id} already has another flight at that time!")
            return None;
        if (departure_time < f.arrival_time and arrival_time > f.departure_time) and plane_id == f.plane_id:
            print(f"Plane {plane_id} already has another flight at that time!")
            return None;
        
    new_flight = Flight(departure_time=departure_time, arrival_time=arrival_time, plane_id=plane_id, pilot_id=pilot_id, departure_destination=departure_destination, destination=destination)
    db.session.add(new_flight)
    db.session.commit()
    return new_flight

def get_all_flights_json(page,per_page,destination=None,sort=None):
    query = Flight.query
    #filtering
    if destination:
        query = Flight.query.filter_by(destination=destination)
    
    #sort
    if sort:
        descending = sort.startswith('-')
        field_name = sort.lstrip('-')
        if hasattr(Flight,field_name):
            column = getattr(Flight,field_name)
            query = query.order_by(column.desc() if descending else column.asc())
        
    paginated = query.paginate(page=page,per_page=per_page,error_out=False)
    return {
        "data": [flights.get_json() for flights in paginated.items],
        "page":paginated.page,
        "per_page":paginated.per_page,
        "total":paginated.total,
        "total_pages":paginated.pages
    }

def get_all_gates_json(page,per_page,sort=None):
    query = Gate.query
    
    #sorting
    if sort:
        descending = sort.startswith('-')
        field_name = sort.lstrip('-')
        if hasattr(Gate,field_name):
            column = getattr(Gate,field_name)
            query = query.order_by(column.desc() if descending else column.asc())
    
    #pagination:
    paginated = query.paginate(page=page,per_page=per_page,error_out=False)
    return {
        "data": [gate.get_json() for gate in paginated.items],
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total": paginated.total,
        "total_pages":paginated.pages
    }
    
def get_all_planes_json(page,per_page,model=None,sort=None):
    query = Plane.query

    #filtering
    if model:
        query = query.filter_by(model=model)
    
    #sorting
    if sort:
        descending = sort.startswith('-')
        field_name = sort.lstrip('-')
        if hasattr(Plane,field_name):
            column = getattr(Plane,field_name)
            query = query.order_by(column.desc() if descending else column.asc())
    
    #pagination
    paginated = query.paginate(page=page,per_page=per_page,error_out=False)
    return {
        "data": [plane.get_json() for plane in paginated.items],
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total": paginated.total,
        "total_pages":paginated.pages
    }

def get_all_pilots_json(page,per_page,sort=None):
    query = Pilot.query
    
    #sorting
    if sort:
        descending = sort.startswith('-')
        field_name = sort.lstrip('-')
        if hasattr(Pilot,field_name):
            column = getattr(Pilot,field_name)
            query = query.order_by(column.desc() if descending else column.asc())
    
    #pagination
    paginated = query.paginate(page=page,per_page=per_page,error_out=False)
    return {
        "data":[pilot.get_json() for pilot in paginated.items],
        "page":paginated.page,
        "per_page":paginated.per_page,
        "total":paginated.total,
        "total_pages":paginated.pages
    }

def get_all_admins_json():
    admins = Admin.query.all()
    return [admin.get_json() for admin in admins]

def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight:
        gates = Gate.query.all()
        flight_id = int(flight_id)
        for g in gates:
            if g.flight == flight_id:
                print(f"gate deleted")
                db.session.delete(g)
        db.session.delete(flight)
        db.session.commit()
        return True
    return False

#Code to retrieve all flights, gates, planes, and pilots from the database
def get_all_flights():
    return Flight.query.all()

def get_all_gates():
    return Gate.query.all()

def get_all_planes():
    return Plane.query.all()

def get_all_pilots():
    return Pilot.query.all()

#Code to update gate, plane, and pilot information in the database
def update_gate(gate_id,terminal,flight_id):
    flight_id = int(flight_id)
    gate = Gate.query.get(gate_id)
    flight = Flight.query.get(flight_id)
    
    if not flight:
        print(f"Flight ID {flight_id} does not exist.")
        return False  # Flight ID does not exist
    
    Flights = Gate.query.all()
    for f in Flights:
        if f.flight == flight_id and f.id != gate_id:
            print(f"Gate for Flight ID {flight_id} already exists.")
            return None  # Gate for this flight already exists
    
    if gate:
        gate.terminal = terminal
        gate.flight = flight_id
        db.session.commit()
        return True
    else:
        print(f"Gate ID {gate_id} does not exist.")
        
    return False

def update_plane(plane_id,model,capacity):
    plane = Plane.query.get(plane_id)
    if plane:
        plane.model = model
        plane.capacity = capacity
        db.session.commit()
        return True
    return False

def update_pilot(pilot_id,name):
    pilot = Pilot.query.get(pilot_id)
    names = Pilot.query.all()
    for p in names:
        if p.name == name and p.id != pilot_id:
            print(f"Another pilot with name {name} already exists.")
            return False  # Pilot with the same name already exists
    if pilot:
        pilot.name = name
        db.session.commit()
        return True
    return False

def update_flight(departure_time, arrival_time, plane_id, pilot_id, departure_destination, destination, flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        print(f"Flight ID {flight_id} does not exist.")
        return False  # Flight ID does not exist

    plane_id = int(plane_id)
    pilot_id = int(pilot_id)
    plane = Plane.query.get(plane_id)
    if not plane:
        print(f"Plane ID {plane_id} does not exist.")
        return False  # Plane ID does not exist
    pilot = Pilot.query.get(pilot_id)
    if not pilot:
        print(f"Pilot ID {pilot_id} does not exist.")
        return False  # Pilot ID does not exist

    if departure_time >= arrival_time:
        print("Departure time must be before arrival time.")
        return False  # Invalid time range

    Flights = Flight.query.all()
    for f in Flights:
        if f.id != flight_id:  # Exclude the current flight from the check
            if (departure_time < f.arrival_time and arrival_time > f.departure_time) and pilot_id == f.pilot_id:
                print(f"Pilot {pilot_id} already has another flight at that time!")
                return False
            if (departure_time < f.arrival_time and arrival_time > f.departure_time) and plane_id == f.plane_id:
                print(f"Plane {plane_id} already has another flight at that time!")
                return False

    flight.departure_time = departure_time
    flight.arrival_time = arrival_time
    flight.plane_id = plane_id
    flight.pilot_id = pilot_id
    flight.departure_destination = departure_destination
    flight.destination = destination
    db.session.commit()
    return True

#Code to delete gate, plane, and pilot information from the database
def delete_gate(gate_id):
    gate = Gate.query.get(gate_id)  
    if gate:
        db.session.delete(gate)
        db.session.commit()
        return True
    return False

def delete_plane(plane_id):
    plane = Plane.query.get(plane_id)
    flights = Flight.query.all()
    plane_id = int(plane_id)
    if plane:
        for f in flights:
            if f.plane_id == plane_id:
                db.session.delete(f)
        db.session.delete(plane)
        db.session.commit()
        return True
    return False

def delete_pilot(pilot_id):
    pilot = Pilot.query.get(pilot_id)
    flights = Flight.query.all()
    pilot_id = int(pilot_id)
    if pilot:
        for f in flights:
            if f.pilot_id == pilot_id:
                db.session.delete(f)
        db.session.delete(pilot)
        db.session.commit()
        return True
    return False