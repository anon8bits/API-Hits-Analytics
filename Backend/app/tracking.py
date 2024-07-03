from flask import request, g
from .models import APIHit, APIStats
from . import db
import httpagentparser
import re
import time

def generalize_endpoint(endpoint):
    if endpoint.startswith('/api/customers/'):
        if endpoint.startswith('/api/customers/update/'):
            return '/api/customers/update'
        elif endpoint.startswith('/api/customers/delete/'):
            return '/api/customers/delete'
        elif re.match(r'/api/customers/\d+$', endpoint):
            return '/api/customers/:id'
    return endpoint

def setup_tracking(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def track_api_hit(response):
        user_agent = request.headers.get('User-Agent')
        parsed_agent = httpagentparser.detect(user_agent)

        os_info = parsed_agent.get('os', {}).get('name')
        if not os_info:
            os_info = request.user_agent.platform or 'Unknown'
        generalized_endpoint = generalize_endpoint(request.path)

        response_time = time.time() - g.start_time

        hit = APIHit(
            request_type=request.method,
            endpoint=generalized_endpoint,
            user_agent=user_agent,
            request_body=request.get_data(as_text=True),
            os=os_info,
            ip_address=request.remote_addr,
            status_code=response.status_code,
            response_time=response_time
        )
        db.session.add(hit)
        stats = APIStats.query.first()
        if not stats:
            stats = APIStats(total_requests=0, failed_requests=0, total_response_time=0.0)
        db.session.add(stats)
        if stats.total_requests is None:
            stats.total_requests = 0
        if stats.failed_requests is None:
            stats.failed_requests = 0
        if stats.total_response_time is None:
            stats.total_response_time = 0.0

        stats.total_requests += 1
        if response.status_code >= 400:
            stats.failed_requests += 1
        stats.total_response_time += response_time

        db.session.commit()

        return response