import pytest, unittest
from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin
from App.models.Flights import Flight
from App.models.Pilots import Pilot
from App.models.Planes import Plane
from App.models.Gates import Gate
from App.controllers import (
    create_user,
    create_admin,
    get_user_by_username
)


'''
User Tests
'''

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

#Password Hashing
def test_password_hashing():
    user = User("bob","bobpass",False)
    assert user.password != "bobpass"

def test_password_is_correct():
    user = User("bob","bobpass",False)
    assert user.check_password("bobpass")

def test_password_is_incorrect():
    user = User("bob","bobpass",False)
    assert user.check_password("bobpasss") == False

#User and Admin creation
def test_user_creation():
    user = User("bob","bobpass",False)
    assert user.username == "bob"
    assert user.is_admin == False

def test_admin_creation():
    user = User("admin","adminpass",True)
    assert user.username == "admin"
    assert user.is_admin == True

#plane and pilot JSON checks 
def test_pilot_json():
    pilot = Pilot(name="Harry Kane")
    json = pilot.get_json()
    assert "id" in json
    assert "name" in json

def test_plane_json():
    plane = Plane(model="Boeing 737",capacity=180)
    json = plane.get_json()
    assert "id" in json
    assert "model" in json
    assert "capacity" in json

