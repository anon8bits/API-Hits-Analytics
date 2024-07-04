from flask import Blueprint, jsonify, request
from .models import APIHit
from .models import APIStats

analytics_bp = Blueprint('analytics', __name__)

# Endpoint to get number of requests by a certain column

@analytics_bp.route('/api/aggregate/<column_name>', methods=['GET'])
def aggregate_data(column_name):
    try:
        results = APIHit.aggregate_by_column(column_name)
        data = [{'label': str(r.label), 'count': r.count} for r in results]
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
# Endpoint to get the stats for all requests (total requests, avg response time, failed requests)
    
@analytics_bp.route('/api/stats', methods=['GET'])
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
    
# Endpoint to get requests for past req.params.days number of days

@analytics_bp.route('/api/requests', methods=['GET'])
def get_recent_requests():
    days = request.args.get('days', default=30, type=int)
    
    if days <= 0:
        return jsonify({'error': 'Days parameter must be a positive integer'}), 400
    
    requests = APIHit.get_recent_requests(days)
    
    data = [{
        'id': req.id,
        'timestamp': req.timestamp.isoformat(),
        'request_type': req.request_type,
        'endpoint': req.endpoint,
        'status_code': req.status_code,
        'user_agent': req.user_agent,
        'os': req.os,
        'ip_address': req.ip_address
    } for req in requests]
    
    return jsonify(data), 200