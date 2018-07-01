from flask import Flask

from flask_restful import Api

from flasgger import Swagger

from flask_jwt_extended import JWTManager

from resources.requests import requests_bp
from resources.rides import rides_bp
from resources.users import users_bp
from resources.cars import cars_bp

def create_app():
    # Create an instance of the flask application
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Ride My Way',
        'uiversion': 3
    }
    app.config['JWT_SECRET_KEY'] = 'my_secret_key'
    # app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    Swagger(app)
    JWTManager(app)

    app.register_blueprint(requests_bp)
    app.register_blueprint(rides_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(cars_bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

