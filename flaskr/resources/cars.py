from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.models.car import Car

from flaskr.resources.helpers import check_for_empty_fields



class CarListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'registration', type=str, required=True, help='Please enter car registration', location=['form','json']
        )
        self.reqparse.add_argument(
            'model', type=str, required=True, help='Please enter car model', location=['form','json']
        )
        self.reqparse.add_argument(
            'capacity', type=int, required=True, help='Please enter car capacity', location=['form','json']
        )
        super(CarListResource, self).__init__()

    # GET method for car list
    @jwt_required
    def get(self):
        """
        Endpoint for getting a list of all cars
        ---
        tags:
          - Car
        security:
          - Bearer: []  
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There are no cars here'
        """
        return Car.browse()

    # POST method for new car
    @jwt_required
    def post(self):
        """
        Endpoint for creating a car
        ---
        tags:
          - Car
        security:
          - Bearer: []  
        parameters:
          - name: registration
            in: formData
            required: true
            description: The licence plate of the car.
            type: string
          - name: model
            in: formData
            required: true
            description: The model of the car.
            type: string
          - name: capacity
            in: formData
            required: true
            description: The capacity of the car.
            type: integer
        responses:
          500:
            description: Internal server error
          201:
            description: Car created successfully
            # schema:
            #   $ref: '#/definitions/Car'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        car = Car(args['registration'],
                  args['model'], args['capacity'])
        return car.add()


class CarResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'model', type=str, required=True, help='Please enter car model', location=['form','json']
        )
        self.reqparse.add_argument(
            'capacity', type=int, required=True, help='Please enter car capacity', location=['form','json']
        )
        super(CarResource, self).__init__()


    # PUT method for editing a car
    @jwt_required
    def put(self, registration):
        """
        Endpoint for updating a ride offer
        ---
        tags:
          - Car
        security:
          - Bearer: []  
        parameters:
          - name: registration
            in: path
            required: true
            description: The licence plate of the car.
            type: string
          - name: model
            in: formData
            required: true
            description: The model of the car.
            type: string
          - name: capacity
            in: formData
            required: true
            description: The capacity of the car.
            type: integer
        responses:
          500:
            description: Internal server error
          200:
            description: Car updated successful
            schema:
              $ref: '#/definitions/UpdateCar'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return Car.edit(registration, args['model'], args['capacity'])

        
    # GET method for a car
    @jwt_required
    def get(self, registration):
        """
        Endpoint for getting a car's details
        ---
        tags:
          - Car
        security:
          - Bearer: []  
        parameters:
          - name: registration
            in: path
            required: true
            type: string
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There car does not exist
        """
        request = Car.read(registration)
        return {'status':'success', 'message': 'Fetch successful', 'data': request}


    # DELETE method for deleting a car
    @jwt_required
    def delete(self, registration):
        """
        Endpoint for deleting a car
        ---
        tags:
          - Car
        security:
          - Bearer: []  
        parameters:
          - name: registration
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Car successfully deleted
          404:
            description: The car does not exist
        """
        return Car.delete(registration)

cars_bp = Blueprint('resources.car', __name__)
api = Api(cars_bp)
api.add_resource(
    CarResource,
    '/api/v2/cars/<registration>'
)
api.add_resource(
    CarListResource,
    '/api/v2/cars'
    )
