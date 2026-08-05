from .user import create_Flight, create_Pilot, create_Plane, create_admin, create_user, create_Gate
from App.database import db
from datetime import datetime


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', False)
    create_user('alice', 'alicepass', False)
    create_user('admin', 'adminpass', True)
    create_Pilot('John Doe')
    create_Pilot('Bob Dylan')
    create_Pilot('Michael Jackson')
    create_Pilot('Lionel Messi')
    create_Pilot('Harry Kane')
    create_Plane('Boeing 737', 180)
    create_Plane('Boeing 737', 180)
    create_Plane('Boeing 747', 366)
    create_Plane('Boeing 747', 366)
    create_Plane('Airbus A330', 210)
    create_Plane('Airbus A330', 210)
    create_Flight("2024-06-01 10:00:00","2024-06-01 14:00:00", 2, 1, 'New York', 'Los Angeles')
    create_Flight("2026-06-01 10:00:00","2026-07-01 14:00:00", 1, 2, 'Capetown', 'Los Angeles')
    create_Flight("2025-12-28 10:00:00","2025-12-28 18:00:00", 4, 3, 'Japan', 'Paris')
    create_Flight("2023-06-01 23:00:00","2023-06-02 01:00:00", 6, 1, 'Trinidad', 'Barbados')
    create_Flight("2024-06-01 10:00:00","2024-06-01 14:00:00", 3, 5, 'Nigeria', 'London')
    create_Gate('A1', 1)
    create_Gate('A2', 2)
    create_Gate('B1', 3)
    create_Gate('B2', 4)
