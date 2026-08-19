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

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

#Flight creation workflow
'''Test that valid flights can be created'''
def test_create_flight_workflow(empty_db):
    empty_db.post("/api/create_user",json={
        "username": "admin",
        "password": "adminpass",
        "is_admin": True
    })
    empty_db.post("/api/login",json={
        "username": "admin",
        "password": "adminpass"
    })
    empty_db.post("/api/create_pilot",json={
        "name": "Bob Marley"
    })
    empty_db.post("/api/create_plane",json={
        "model": "Boeing 737",
        "capacity": 180
    })
    response = empty_db.post("/api/create_flight",json={
            "departure_time": "2026-07-11 12:00:00",
            "arrival_time": "2026-07-11 14:00:00",
            "pilot_id": 1,
            "plane_id": 1,
            "departure_destination": "Paris",
            "arrival_destination": "Texas"
        })
    assert response.status_code == 201

def test_multiple_flights_creation(empty_db):
    empty_db.post("/api/create_user",json={
            "username": "admin",
            "password": "adminpass",
            "is_admin": True
        })
    empty_db.post("/api/login",json={
            "username": "admin",
            "password": "adminpass"
        })
    empty_db.post("/api/create_pilot",json={
            "name": "Bob Marley"
        })
    empty_db.post("/api/create_plane",json={
            "model": "Boeing 737",
            "capacity": 180
        })
    response_1 = empty_db.post("/api/create_flight",json={
                "departure_time": "2026-07-11 12:00:00",
                "arrival_time": "2026-07-11 14:00:00",
                "pilot_id": 1,
                "plane_id": 1,
                "departure_destination": "Paris",
                "arrival_destination": "Texas"
            })
    assert response_1.status_code == 201
    
    response_2 = empty_db.post("/api/create_flight",json={
                    "departure_time": "2026-07-11 15:00:00",
                    "arrival_time": "2026-07-11 16:00:00",
                    "pilot_id": 1,
                    "plane_id": 1,
                    "departure_destination": "Paris",
                    "arrival_destination": "Texas"
                })
    assert response_2.status_code == 201
    
    response_3 = empty_db.post("/api/create_flight",json={
                    "departure_time": "2026-07-11 17:00:00",
                    "arrival_time": "2026-07-11 18:00:00",
                    "pilot_id": 1,
                    "plane_id": 1,
                    "departure_destination": "Paris",
                    "arrival_destination": "Texas"
                })
    assert response_3.status_code == 201

#