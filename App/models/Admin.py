from App import db
from .user import User

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    def __init__(self, username, password,is_admin):
        super().__init__(username, password, is_admin=True)
    
    def get_json(self):
        return {
            'id':self.id,
            'username':self.username,
        }