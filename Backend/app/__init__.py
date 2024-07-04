import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models
        from .customers import customers_bp
        from .tracking import setup_tracking
        from .analytics import analytics_bp

        app.register_blueprint(customers_bp)
        app.register_blueprint(analytics_bp)
        setup_tracking(app)

    return app
