from flask import Flask

from flask_restful import Api

from resources.rides import rides_bp
from resources.requests import requests_bp
from resources.users import users_bp

def create_app(configObject):
    # Create an instance of the flask application
    app = Flask(__name__)
    app.config.from_object(configObject)

    app.register_blueprint(requests_bp)
    app.register_blueprint(rides_bp)
    app.register_blueprint(users_bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

