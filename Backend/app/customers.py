from flask import Blueprint, request, jsonify
from .models import Customer
from . import db

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/api/customers/all', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customers_bp.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict()), 200

@customers_bp.route('/api/customers/create', methods=['POST'])
def create_customer():
    data = request.json
    if not all(key in data for key in ('first_name', 'last_name', 'email')):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_customer = Customer(**data)
    
    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@customers_bp.route('/api/customers/delete/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": f"Customer {customer_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@customers_bp.route('/api/customers/update/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.json
    
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    
    try:
        db.session.commit()
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
from .models import APIStats

@customers_bp.route('/api/stats', methods=['GET'])
def get_api_stats():
    stats = APIStats.query.first()
    if not stats:
        return jsonify({"error": "No stats available"}), 404
    
    avg_response_time = stats.total_response_time / stats.total_requests if stats.total_requests > 0 else 0
    
    return jsonify({
        "total_requests": stats.total_requests,
        "failed_requests": stats.failed_requests,
        "average_response_time": avg_response_time
    }), 200