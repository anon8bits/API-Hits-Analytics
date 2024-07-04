from flask import request, g, Blueprint, jsonify
from .models import APIHit, APIStats
from . import db
import httpagentparser
import re
import time

def get_browser_info(user_agent):
    parsed = httpagentparser.detect(user_agent)
    browser = parsed.get('browser', {})
    return browser.get('name', 'Unknown')

def generalize_endpoint(endpoint):
    if endpoint.startswith('/api/customers/'):
        if endpoint.startswith('/api/customers/update/'):
            return '/api/customers/update'
        elif endpoint.startswith('/api/customers/delete/'):
            return '/api/customers/delete'
        elif re.match(r'/api/customers/\d+$', endpoint):
            return '/api/customers/:id'
    return endpoint

def should_track_endpoint(endpoint):
    return endpoint.startswith('/api/customers/')

def setup_tracking(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def track_api_hit(response):
        if not should_track_endpoint(request.path):
            return response

        user_agent = request.headers.get('User-Agent')
        parsed_agent = httpagentparser.detect(user_agent)
        browser_info = get_browser_info(user_agent)
        os_info = parsed_agent.get('os', {}).get('name')
        if not os_info:
            os_info = request.user_agent.platform or 'Unknown'
        generalized_endpoint = generalize_endpoint(request.path)

        response_time = time.time() - g.start_time

        hit = APIHit(
            request_type=request.method,
            endpoint=generalized_endpoint,
            user_agent=browser_info,
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
        
        stats.total_requests = (stats.total_requests or 0) + 1
        if response.status_code >= 400:
            stats.failed_requests = (stats.failed_requests or 0) + 1
        stats.total_response_time = (stats.total_response_time or 0.0) + response_time

        db.session.commit()

        return response