import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.models.ride import Ride

from flaskr.resources.helpers import check_for_empty_fields, validate_date


class RideListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, required=True, help='Please enter dropoff', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'pickup', type=str, required=True, help='Please enter pickup', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'time', type=str, required=True, help='Please enter time', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'price', type=float, required=True, help='Please enter price', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'date', type=str, required=True, help='Please enter the date', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'driver_id', type=int, required=True, help='Please enter the driver', location=['form', 'json']
        )
        super(RideListResource, self).__init__()

    # GET method for ride list
    @jwt_required
    def get(self):
        """
        Endpoint for getting a list of all ride offers
        ---
        tags:
          - Ride
        security:
          - Bearer: []  
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There are no rides offers yet'
        """
        return Ride.browse()

    # POST method for new ride request
    @jwt_required
    def post(self):
        """
        Endpoint for creating a ride offer
        ---
        tags:
          - Ride
        security:
          - Bearer: []
        parameters:
          - name: date
            in: formData
            required: true
            description: Date the ride will be taken.
            type: string
            format: date
          - name: time
            in: formData
            required: true
            description: Time the ride will start.
            type: string
          - name: pickup
            in: formData
            required: true
            description: Place the ride will be taken from.
            type: string
          - name: dropoff
            in: formData
            required: true
            description: Destination of the ride.
            type: string
          - name: driver_id
            in: formData
            required: true
            description: Unique identifier of the driver.
            type: integer
          - name: price
            in: formData
            required: true
            description: The price of the ride.
            type: integer
            format: float
        responses:
          500:
            description: Internal server error
          201:
            description: Ride creation successful
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        validate_date(args['date'])
        ride = Ride(
            args['date'],
            args['time'],
            args['pickup'],
            args['dropoff'],
            args['driver_id'],
            args['price']
        )
        return ride.add()


class RideResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, required=True, help='Please enter dropoff', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'pickup', type=str, required=True, help='Please enter pickup', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'time', type=str, required=True, help='Please enter time', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'price', type=float, required=True, help='Please enter price', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'date', type=str, required=True, help='Please enter the date', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'driver_id', type=int, required=True, help='Please enter the driver', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'status', type=str, required=False, help='Please enter the ride status', default=Ride.STATUS_STARTED, location=['form', 'json']
        )

        super(RideResource, self).__init__()


    # PUT method for editing a ride request

    @jwt_required
    def put(self, ride_id):
        """
        Endpoint for updating a ride offer
        ---
        tags:
          - Ride
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
            description: Unique identifier of the ride.
            type: integer
          - name: date
            in: formData
            required: true
            description: Date the ride will be taken.
            type: string
          - name: time
            in: formData
            required: true
            description: Time the ride will start.
            type: string
          - name: pickup
            in: formData
            required: true
            description: Place the ride will be taken from.
            type: string
          - name: dropoff
            in: formData
            required: true
            description: Destination of the ride.
            type: string
          - name: driver_id
            in: formData
            required: true
            description: Unique identifier of the driver.
            type: integer
          - name: price
            in: formData
            required: true
            description: The price of the ride.
            type: integer
            format: float
          - name: status
            in: formData
            description: The status of the ride.
            type: string
            enum:
              - "In Offer"
              - "Started"
              - "Done"
        responses:
          500:
            description: Internal server error
          201:
            description: Ride creation successful
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return Ride.edit(
                    args['date'], 
                    args['time'], 
                    args['pickup'], 
                    args['dropoff'], 
                    args['driver_id'], 
                    args['price'], 
                    args['status'], 
                    ride_id
                )
        
    # GET method for a ride request
    @jwt_required
    def get(self, ride_id):
        """
        Endpoint for getting a ride offer's details
        ---
        tags:
          - Ride
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There ride offer does not exist
        """
        request = Ride.read(ride_id)
        return {'status':'success', 'message': 'Fetch successful', 'data': request}


    # DELETE method for deleting a ride request
    @jwt_required
    def delete(self, ride_id):
        """
        Endpoint for deleting a ride
        ---
        tags:
          - Ride
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Ride successfully deleted
          404:
            description: The ride offer does not exist
        """
        return Ride.delete(ride_id)

rides_bp = Blueprint('resources.rides', __name__)
api = Api(rides_bp)
api.add_resource(
    RideResource, 
    '/api/v2/rides/<ride_id>'
)
api.add_resource(
    RideListResource, 
    '/api/v2/rides'
    )
