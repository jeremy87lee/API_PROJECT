from App.database import db

class Pilot(db.Model):
    __tablename__ = 'pilot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    def get_json(self):
        return {
            'id': self.id,
            'name': self.name
        }