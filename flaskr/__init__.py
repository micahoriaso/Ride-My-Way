from flask import Flask

from flask_restful import Api

from resourcesV1.rides import rides_v1_bp
from resourcesV1.requests import requests_v1_bp
from resourcesV1.users import users_v1_bp

from resourcesV2.requests import requests_v2_bp
from resourcesV2.rides import rides_v2_bp
from resourcesV2.users import users_v2_bp

from flaskr.db import create_tables


def create_app(test_config=None):
    # Create an instance of the flask application
    app = Flask(__name__)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='my-very-long-secret-key',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    app.register_blueprint(requests_v1_bp)
    app.register_blueprint(rides_v1_bp)
    app.register_blueprint(users_v1_bp)

    app.register_blueprint(requests_v2_bp)
    app.register_blueprint(rides_v2_bp)
    app.register_blueprint(users_v2_bp)

    if __name__ == '__main__':
        app.run(debug=True)

        
    return app

