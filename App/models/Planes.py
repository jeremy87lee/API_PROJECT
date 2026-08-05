from App.database import db

class Plane(db.Model):
    __tablename__ = 'plane'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    def get_json(self):
        return {
            'id': self.id,
            'model': self.model,
            'capacity': self.capacity
        }