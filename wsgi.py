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
@click.argument("is_admin",default=False)
def create_user_command(username,password,is_admin):
    response = requests.post(
        "http://127.0.0.1:8080/api/create_user",
        json={"username": username,"password":password,"is_admin":is_admin}
    )
    print(response.json().get("message"))

@cli_client.command("login",help="Command to login a user")
@click.argument("username",default="admin")
@click.argument("password",default="adminpass")
def login_command(username,password):
    response = requests.post(
        "http://127.0.0.1:8080/api/login",
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
        "http://127.0.0.1:8080/api/flights",
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
        "http://127.0.0.1:8080/api/create_flight",
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
        "http://127.0.0.1:8080/api/update_flight/"+str(flight_id),  
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
    