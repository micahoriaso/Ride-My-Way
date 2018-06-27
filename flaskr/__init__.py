from flask import Flask

from flask_restful import Api

from resourcesV1.rides import rides_v1_bp
from resourcesV1.requests import requests_v1_bp
from resourcesV1.users import users_v1_bp

from resourcesV2.requests import requests_v2_bp
from resourcesV2.rides import rides_v2_bp
from resourcesV2.users import users_v2_bp

def create_app(configObject):
    # Create an instance of the flask application
    app = Flask(__name__)
    app.config.from_object(configObject)

    app.register_blueprint(requests_v1_bp)
    app.register_blueprint(rides_v1_bp)
    app.register_blueprint(users_v1_bp)

    app.register_blueprint(requests_v2_bp)
    app.register_blueprint(rides_v2_bp)
    app.register_blueprint(users_v2_bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

