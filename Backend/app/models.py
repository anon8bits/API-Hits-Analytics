from datetime import datetime, timedelta
from . import db
from sqlalchemy import func

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
    @classmethod
    def aggregate_by_column(cls, column_name):
        valid_columns = ['request_type', 'endpoint', 'user_agent', 'os', 'status_code']
        if column_name not in valid_columns:
            raise ValueError(f"Invalid column name. Must be one of {valid_columns}")
        
        column = getattr(cls, column_name)
        query = db.session.query(
            column.label('label'),
            func.count(func.distinct(cls.id)).label('count')
        ).group_by(column)
        
        return query.all()
    @classmethod
    def get_recent_requests(cls, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = cls.query.filter(
            cls.timestamp.between(start_date, end_date)
        ).order_by(cls.timestamp.desc())
        
        return query.all()

class APIStats(db.Model):
    __tablename__ = 'api_stats'
    id = db.Column(db.Integer, primary_key=True)
    total_requests = db.Column(db.Integer, default=0, nullable=False)
    failed_requests = db.Column(db.Integer, default=0, nullable=False)
    total_response_time = db.Column(db.Float, default=0.0, nullable=False)
