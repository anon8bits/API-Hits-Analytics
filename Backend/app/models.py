from datetime import datetime
from . import db

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

class APIHit(db.Model):
    __tablename__ = 'api_hits'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    request_type = db.Column(db.String(10))
    endpoint = db.Column(db.String(255))
    user_agent = db.Column(db.String(255))
    request_body = db.Column(db.Text)
    os = db.Column(db.String(50))
    ip_address = db.Column(db.String(50))
