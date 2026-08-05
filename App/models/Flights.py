from App.database import db
from App.models.Pilots import Pilot
from App.models.Planes import Plane

class Flight(db.Model):
    __tablename__ = 'flight'
    id = db.Column(db.Integer, primary_key=True)
    plane_id = db.Column(db.Integer, db.ForeignKey('plane.id'), nullable=False)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilot.id'), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    departure_destination = db.Column(db.String(50), nullable=True)
    destination = db.Column(db.String(50), nullable=True)
    
    plane = db.relationship('Plane', backref=db.backref('flights', lazy=True))
    pilot = db.relationship('Pilot', backref=db.backref('flights', lazy=True))
    
    def get_json(self):
        
        return {
            'id': self.id,
            'plane': self.plane.model,
            'pilot': self.pilot.name,
            'arrival_time': self.arrival_time,
            'departure_time': self.departure_time,
            'departure_destination': self.departure_destination,
            'destination': self.destination
        }