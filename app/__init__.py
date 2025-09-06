from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.utils.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config.get_config())

    db.init_app(app)
    CORS(app, resources={r"/generate_exam": {"origins": app.config['SPRING_URL']}})
    with app.app_context():
        from app.routes import init_routes
        init_routes(app)

    return app
