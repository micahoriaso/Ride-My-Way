from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.models.car import Car

from flaskr.resources.helpers import check_for_empty_fields



class CarListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'registration', type=str, required=True, help='Please enter car registration', location='json'
        )
        self.reqparse.add_argument(
            'model', type=str, required=True, help='Please enter car model', location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=str, required=True, help='Please enter car capacity', location='json'
        )
        super(CarListResource, self).__init__()
        self.car = Car()

    # GET method for ride list
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
          202:
            description: There are no cars here'
        """
        return self.car.browse()

    # POST method for new ride request
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
          - name: body
            in: body
            required: true
            schema:
              id: Car
              required:
                - registration
                - model
                - capacity
              properties:
                registration:
                  type: string
                  description: The licence plate of the car.
                model:
                  type: string
                  description: The model of the car.
                capacity:
                  type: integer
                  description: The capacity of the car.
        responses:
          500:
            description: Internal server error
          201:
            description: Car created successfully
            schema:
              $ref: '#/definitions/Car'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        self.car.abort_if_car_registration_is_already_used(
            args['registration'])
        return self.car.add(args['registration'],
                           args['model'], args['capacity'])


class CarResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'model', type=str, required=True, help='Please enter car model', location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=str, required=True, help='Please enter car capacity', location='json'
        )
        self.car = Car()
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
          - name: body
            in: body
            required: true
            schema:
              id: UpdateCar
              required:
                - model
                - capacity
              properties:
                model:
                  type: string
                  description: The car's model
                capacity:
                  type: integer
                  description: The car's capacity.
        responses:
          500:
            description: Internal server error
          200:
            description: Car updated successful
            schema:
              $ref: '#/definitions/UpdateCar'
        """
        self.car.abort_if_car_doesnt_exist(registration)
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return self.car.edit(registration, args['model'], args['capacity'])

        
    # GET method for a ride request

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
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There car does not exist
        """
        request = self.car.abort_if_car_doesnt_exist(registration)
        return {'status':'success', 'message': 'Fetch successful', 'data': request}


    # DELETE method for deleting a ride request

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
        self.car.abort_if_car_doesnt_exist(registration)
        return self.car.delete(registration)

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
