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
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)

class APIStats(db.Model):
    __tablename__ = 'api_stats'
    id = db.Column(db.Integer, primary_key=True)
    total_requests = db.Column(db.Integer, default=0, nullable=False)
    failed_requests = db.Column(db.Integer, default=0, nullable=False)
    total_response_time = db.Column(db.Float, default=0.0, nullable=False)
