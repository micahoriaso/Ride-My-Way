from flask import Flask

from flask_restful import Api

from resources.rides import RideResource, RideListResource
from resources.requests import RequestResource, RequestListResource

def create_app(test_config=None):
    # Create an instance of the flask application
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    api = Api(app)
    api.add_resource(RideResource, '/api/v1/rides/<ride_id>')
    api.add_resource(RideListResource, '/api/v1/rides/',
                     '/api/v1/rides/<ride_id>')
    api.add_resource(RequestResource, '/api/v1/rides/<ride_id>/requests/<request_id>')
    api.add_resource(RequestListResource, '/api/v1/rides/<ride_id>/requests',
                     '/api/v1/rides/<ride_id>/requests/<request_id>')
    
    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

