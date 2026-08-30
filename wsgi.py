from urllib import response

import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
import requests, json


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/test_units.py","-v"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/test_integration.py","-v"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

cli_client = AppGroup('cli_client',help='CLI client for API project')
app.cli.add_command(cli_client)

@cli_client.command("create user",help="Command to create a new user")
@click.argument("username",default="jeremy")
@click.argument("password",default="jeremypass")
def create_user_command(username,password):
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_user",
        json={"username": username,"password":password}
    )
    print(response.json().get("message"))

@cli_client.command("create admin",help="Command to create a new admin user")
@click.argument("username",default="admin")
@click.argument("password",default="adminpass")
def create_admin_command(username,password):
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_admin",
        json={"username": username,"password":password}
    )
    print(response.json().get("message"))

@cli_client.command("login",help="Command to login a user")
@click.argument("username",default="admin")
@click.argument("password",default="adminpass")
def login_command(username,password):
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/login",
        json={"username":username,"password":password}
    )
    if(response.ok):
        print("Logged in!")
        print(response.json())
        save_token(response.json().get("access_token"))
    else:
        print(response.json().get("message"))

def save_token(token):
    with open(".cli_token.json","w") as f:
        json.dump({"token":token},f)

def load_token():
    try: 
        with open(".cli_token.json","r") as f:
            data = json.load(f)
            return data.get("token")
    except FileNotFoundError:
        return None


""" Flight commands """
@cli_client.command("list flights",help="Lists all flights")
@click.argument("page",default=1)
@click.argument("per_page",default=5)
@click.argument("destination",default="Los Angeles")
@click.argument("sort",default="-departure_time")
def list_flights(page,per_page,destination,sort):
    token = load_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(
        "https://api-project-chbu.onrender.com/api/flights",
        params={"page":page,
                "per_page":per_page,
                "destination":destination,
                "sort":sort}, headers=headers
    )
    print(response.json().get("data"))

@cli_client.command("create flight",help="Creates a flight")
@click.argument("plane_id",default=1)
@click.argument("pilot_id",default=1)
@click.argument("departure_time",default="2026-08-25 10:00:00")
@click.argument("arrival_time",default="2026-08-25 12:30:00")
@click.argument("departure_destination",default="Trinidad")
@click.argument("destination",default="Antigua")
def create_flight_command(plane_id,pilot_id,departure_destination,destination,departure_time,arrival_time):
    token = load_token()
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_flight",
        json= {
            "plane_id":plane_id,
            "pilot_id":pilot_id,
            "departure_destination":departure_destination,
            "arrival_destination":destination,
            "departure_time":departure_time,
            "arrival_time":arrival_time
        },
        headers = {"Authorization": f"Bearer {token}"} if token else {}
    )
    if response.ok:
        print("Flight created!")
    else:
        print(response.json().get("message"))

@cli_client.command("update flight",help="update a flight")
@click.argument("flight_id",default=1)
@click.argument("plane_id",default=1)
@click.argument("pilot_id",default=1)
@click.argument("departure_time",default="2026-08-25 23:00:00")
@click.argument("arrival_time",default="2027-08-25 02:30:00")
@click.argument("departure_destination",default="Trinidad")
@click.argument("destination",default="Antigua")
def update_flight_command(plane_id,pilot_id,departure_destination,destination,departure_time,arrival_time,flight_id):
    token = load_token()
    response = requests.put(
        "https://api-project-chbu.onrender.com/api/update_flight/"+str(flight_id),  
        headers={"Authorization": f"Bearer {token}"} if token else {},
        json={
            "plane_id":plane_id,
            "pilot_id":pilot_id,
            "departure_destination":departure_destination,
            "destination":destination,
            "departure_time":departure_time,
            "arrival_time":arrival_time     
        } 
    )
    if response.ok:
        print("flight number "+str(flight_id)+" updated!")
    else:
        print(response.json().get("message"))

@cli_client.command("delete flight",help="Delete a flight")
@click.argument("flight_id",default=1)
def delete_flight_command(flight_id):
    token = load_token()
    response = requests.delete(
        "https://api-project-chbu.onrender.com/api/delete_flight/"+str(flight_id),
        headers={"Authorization": f"Bearer {token}"} if token else {}
    )
    if response.ok:
        print("Flight number "+str(flight_id)+" deleted!")
    else:
        print(response.json().get("message"))

""" Plane commands """

@cli_client.command("list planes",help="List all planes")
@click.argument("page",default=1)
@click.argument("per_page",default=3)
@click.argument("model",default="")
@click.argument("sort",default="-capacity")
def list_planes_command(page,per_page,model,sort):
    token = load_token()
    response = requests.get(
        "https://api-project-chbu.onrender.com/api/planes",
        headers={"Authorization":f"Bearer {token}"} if token else {},
        params={
            "page":page,
            "per_page":per_page,
            "model":model,
            "sort":sort
        })
    if response.ok:
        print(response.json().get("data"))   
    else:
        print("could not display!") 

@cli_client.command("create plane",help="Create a plane")
@click.argument("model",default="Boeing 737")
@click.argument("capacity",default="180")
def create_plane_command(model,capacity):
    token = load_token()
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_plane",
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "model":model,
            "capacity":capacity
        }
    )
    if response.ok:
        print("a "+model+" was created!")
    else:
        print(response.json().get("message"))

@cli_client.command("update plane",help="Update a plane")
@click.argument("plane_id",default=1)
@click.argument("model",default="Boeing 747")
@click.argument("capacity",default="360")
def update_plane_command(model,capacity,plane_id):
    token = load_token()
    response = requests.put(
        "https://api-project-chbu.onrender.com/api/update_plane/"+str(plane_id),
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "model":model,
            "capacity":capacity
        }
    )
    if response.ok:
        print("plane "+str(plane_id)+" was updated!")
    else:
        print(response.json().get("message"))

@cli_client.command("delete plane",help="Delete a plane")
@click.argument("plane_id",default=1)
def delete_plane_command(plane_id):
    token = load_token()
    response = requests.delete(
        "https://api-project-chbu.onrender.com/api/delete_plane/"+str(plane_id),
        headers={"Authorization":f"Bearer {token}" if token else {}}
    )
    if response.ok:
        print("plane "+str(plane_id)+" was deleted!")
    else:
        print(response.json().get("message"))

""" Pilot commands """
@cli_client.command("list pilots",help="List all pilots")
@click.argument("page",default=1)
@click.argument("per_page",default=3)
@click.argument("sort",default="name")
def list_pilots_command(page,per_page,sort):
    token = load_token()
    response = requests.get(
        "https://api-project-chbu.onrender.com/api/pilots",
        headers={"Authorization":f"Bearer {token}" if token else {}},
        params={
            "page":page,
            "per_page":per_page,
            "sort":sort
        }
    )
    if response.ok:
        print(response.json().get("data"))
    else:
        print("Could not display pilots!")

@cli_client.command("create pilot",help="Create a pilot")
@click.argument("name",default="Chris Gayle")
def create_pilot_command(name):
    token = load_token()
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_pilot",
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "name":name
        }
    )
    if response.ok:
        print("Pilot created!")
    else:
        print(response.json().get("message"))

@cli_client.command("update pilot",help="Update a pilot")
@click.argument("pilot_id",default=1)
@click.argument("name",default="Henry James")
def update_pilot_command(name,pilot_id):
    token = load_token()
    response = requests.put(
        "https://api-project-chbu.onrender.com/api/update_pilot/"+str(pilot_id),
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "name":name
        }
    )
    if response.ok:
        print("Pilot "+str(pilot_id)+" updated!")
    else:
        print(response.json().get("message"))

@cli_client.command("delete pilot",help="Delete a pilot")
@click.argument("pilot_id",default=1)
def delete_pilot_command(pilot_id):
    token = load_token()
    response = requests.delete(
        "https://api-project-chbu.onrender.com/api/delete_pilot/"+str(pilot_id),
        headers={"Authorization":f"Bearer {token}" if token else {}}
    )
    if response.ok:
        print("Pilot "+str(pilot_id)+" deleted!")
    else:
        print(response.json().get("message"))

'''Gate Commands'''

@cli_client.command("list gates",help="List all gates")
@click.argument("page",default=1)
@click.argument("per_page",default=3)
@click.argument("sort",default="-terminal")
def list_gates_command(page,per_page,sort):
    token = load_token()
    response = requests.get(
        "https://api-project-chbu.onrender.com/api/gates",
        headers={"Authorization":f"Bearer {token}" if token else{}},
        params={
            "page":page,
            "per_page":per_page,
            "sort":sort
        }   
    )
    if response.ok:
        print(response.json().get("data"))
    else:
        print("could not list gates!")

@cli_client.command("create gate",help="Create a gate")
@click.argument("flight_id",default=5)
@click.argument("terminal",default="A1")
def create_gate_command(flight_id,terminal):
    token = load_token()
    response = requests.post(
        "https://api-project-chbu.onrender.com/api/create_gate",
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "terminal":terminal,
            "flight_id":flight_id
        }
    )
    if response.ok:
        print("Gate created for terminal "+terminal)
    else:
        print(response.json().get("message"))

@cli_client.command("update gate",help="Update a gate")
@click.argument("gate_id",default=4)
@click.argument("flight_id",default=5)
@click.argument("terminal",default="A1")
def update_gate_command(flight_id,terminal,gate_id):
    token = load_token()
    response = requests.put(
        "https://api-project-chbu.onrender.com/api/update_gate/"+str(gate_id),
        headers={"Authorization":f"Bearer {token}" if token else {}},
        json={
            "terminal":terminal,
            "flight_id":flight_id
        }
    )
    if response.ok:
        print("Gate "+str(gate_id)+" updated!")
    else:
        print(response.json().get("message"))

@cli_client.command("delete gate",help="delete a gate")
@click.argument("gate_id",default=2)
def delete_gate_command(gate_id):
    token = load_token()
    response = requests.delete(
        "https://api-project-chbu.onrender.com/api/delete_gate/"+str(gate_id),
        headers={"Authorization":f"Bearer {token}" if token else {}}
    )
    if response.ok:
        print("Gate "+str(gate_id)+" deleted!")
    else:
        print(response.json().get("message"))