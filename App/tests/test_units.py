import pytest, unittest
from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    create_admin
)

'''
User Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_get_users(empty_db):
    response = empty_db.get('/api/users')
    assert response.status_code == 200
    

def test_create_user(empty_db):
        response = empty_db.post('/api/create_user',json={
            "username": "greg",
            "password": "gregpass",
            "is_admin": False
        })
        assert response.status_code == 201
        assert "User created!" == response.get_json().get("message")

def test__user_creation_missing_credentials(empty_db):
    response = empty_db.post('/api/create_user',json={
                "password": "gregpass",
                "is_admin": False
            })
    assert response.status_code == 400
    assert "Missing credentials!" == response.get_json().get("message")
    
def test_user_creation_username_taken(empty_db):
    empty_db.post("/api/create_user",json={
        "username": "bob",
        "password": "bobpass",
        "is_admin": False
    })
    
    response = empty_db.post("/api/create_user",json={
            "username": "bob",
            "password": "bobpass",
            "is_admin": False
        })
    
    assert response.status_code == 409
    assert response.get_json().get("message") == "Username already taken!"

def test_user_login(empty_db):
    response = empty_db.post("/api/login",json={
        "username": "bob",
        "password": "bobpass"
    })
    assert "access_token" in response.get_json()

def test_user_login_bad_credentials(empty_db):
    response = empty_db.post("/api/login",json={
            "username": "bob1",
            "password": "bobpass"
        })
    assert "access_token" not in response.get_json()
    assert response.get_json().get("message") == "bad username or password given"

def test_create_admin(empty_db):
    response = empty_db.post("/api/create_user",json={
                "username": "admin",
                "password": "adminpass",
                "is_admin": True
            })
    assert response.status_code == 201
    assert "User created!" == response.get_json().get("message")

def test_admin_login(empty_db):
    response = empty_db.post("/api/login",json={
        "username": "admin",
        "password": "adminpass"
    })
    assert "access_token" in response.get_json()


'''
Pilot Tests
'''
def test_get_pilots(empty_db):
    response = empty_db.get("/api/pilots")
    assert response.status_code == 200

def test_create_pilot(empty_db):
    response = empty_db.post("/api/create_pilot",json={
        "name": "Harry Kane"
    })
    assert response.status_code == 201
    assert response.get_json().get("message") == "Pilot created!"

def test_create_pilot_missing_credentials(empty_db):
    response = empty_db.post("/api/create_pilot",json={
        
    })
    assert response.status_code == 400
    assert response.get_json().get("message") == "Name not given!"

def test_create_pilot_name_taken(empty_db):
    response = empty_db.post("/api/create_pilot",json={
            "name": "Harry Kane"
    })
    assert response.status_code == 400
    assert response.get_json().get("message") == "Pilot could not be created!"

def test_create_pilot_not_authorized(empty_db):
    empty_db.post("/api/login",json={
        "username": "greg",
        "password": "gregpass"
    })
    response = empty_db.post("/api/create_pilot",json={
        "name": "Bobby Brown"
    })
    assert response.status_code == 401
    assert response.get_json().get("message") == "Only admins can create pilots!"

'''
Plane Tests
'''



'''
Flight Tests
'''
def test_get_flights(empty_db):
    response = empty_db.get("/api/flights")
    assert response.status_code == 200
    assert "data" in response.get_json()

@pytest.mark.skip(reason="Pilots and Planes not created yet!")
def test_create_flight(empty_db):
    response = empty_db.post("/api/create_flight",json={
        "departure_time": "2026-07-11 12:00:00",
        "arrival_time": "2026-07-11 14:00:00",
        "pilot_id": 2,
        "plane_id": 3,
        "departure_destination": "Paris",
        "arrival_destination": "Texas"
    })
    assert response.status_code == 201
    assert response.get_json().get("message") == "Flight created!"