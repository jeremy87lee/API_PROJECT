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

