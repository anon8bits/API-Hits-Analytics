from flask import request
from .models import APIHit
from . import db
import httpagentparser
import re

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
    def track_api_hit():
        user_agent = request.headers.get('User-Agent')
        parsed_agent = httpagentparser.detect(user_agent)

        os_info = parsed_agent.get('os', {}).get('name')
        if not os_info:
            os_info = request.user_agent.platform or 'Unknown'
        generalized_endpoint = generalize_endpoint(request.path)

        hit = APIHit(
            request_type=request.method,
            endpoint=generalized_endpoint,
            user_agent=user_agent,
            request_body=request.get_data(as_text=True),
            os=os_info,
            ip_address=request.remote_addr
        )
        db.session.add(hit)
        db.session.commit()