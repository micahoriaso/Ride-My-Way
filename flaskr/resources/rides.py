import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.models.ride import Ride

from flaskr.resources.helpers import check_for_empty_fields


class RideListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, required=True, help='Please enter dropoff', location='json'
        )
        self.reqparse.add_argument(
            'pickup', type=str, required=True, help='Please enter pickup', location='json'
        )
        self.reqparse.add_argument(
            'time', type=str, required=True, help='Please enter time', location='json'
        )
        self.reqparse.add_argument(
            'price', type=float, required=True, help='Please enter price', location='json'
        )
        self.reqparse.add_argument(
            'date', type=str, required=True, help='Please enter the date', location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=int, required=True, help='Please enter the vehicle capacity', location='json'
        )
        self.reqparse.add_argument(
            'available_seats', type=int, required=True, help='Please enter the available seats', location='json'
        )
        self.reqparse.add_argument(
            'driver_id', type=int, required=True, help='Please enter the driver', location='json'
        )
        self.reqparse.add_argument(
            'registration', type=str, required=True, help='Please enter the registration', location='json'
        )
        self.reqparse.add_argument(
            'status', type=str, required=False, help='Please enter the ride status', default='In Offer', location='json'
        )
        self.ride = Ride()
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
          200:
            description: Fetch successfull
          204:
            description: There are no rides offers yet'
        """
        return self.ride.browse()

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
          - name: body
            in: body
            required: true
            schema:
              id: Ride
              required:
                - date
                - time
                - pickup
                - dropoff
                - capacity
                - seats_available
                - driver_id
                - registration
                - price
                - status
              properties:
                date:
                  type: string
                  description: Date the ride will be taken.
                time:
                  type: string
                  description: Time the ride will start.
                pickup:
                  type: string
                  description: Place the ride will be taken from.
                dropoff:
                  type: string
                  description: Destination of the ride.
                capacity:
                  type: string
                  description: The car's passenger capacity.
                seats_available:
                  type: string
                  description: The seats that are still on offer.
                driver_id:
                  type: string
                  description: Unique identifier of the driver.
                registration:
                  type: string
                  description: The car's licence plate.
                price:
                  type: string
                  description: The price of the ride.
                status:
                  type: string
                  description: The status of the ride.
        responses:
          201:
            description: Ride creation successful
            schema:
              $ref: '#/definitions/Ride'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return self.ride.add(
                    args['date'], 
                    args['time'], 
                    args['pickup'], 
                    args['dropoff'], 
                    args['capacity'], 
                    args['available_seats'], 
                    args['driver_id'], 
                    args['registration'], 
                    args['price'], 
                    args['status']
                )


class RideResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, required=True, help='Please enter dropoff', location='json'
        )
        self.reqparse.add_argument(
            'pickup', type=str, required=True, help='Please enter pickup', location='json'
        )
        self.reqparse.add_argument(
            'time', type=str, required=True, help='Please enter time', location='json'
        )
        self.reqparse.add_argument(
            'price', type=float, required=True, help='Please enter price', location='json'
        )
        self.reqparse.add_argument(
            'date', type=str, required=True, help='Please enter the date', location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=int, required=True, help='Please enter the vehicle capacity', location='json'
        )
        self.reqparse.add_argument(
            'available_seats', type=int, required=True, help='Please enter the available seats', location='json'
        )
        self.reqparse.add_argument(
            'driver_id', type=int, required=True, help='Please enter the driver', location='json'
        )
        self.reqparse.add_argument(
            'registration', type=str, required=True, help='Please enter the registration', location='json'
        )
        self.reqparse.add_argument(
            'status', type=str, required=False, help='Please enter the ride status', default='In Offer', location='json'
        )

        self.ride = Ride()
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
          - name: body
            in: body
            required: true
            schema:
              id: Ride
              required:
                - date
                - time
                - pickup
                - dropoff
                - capacity
                - seats_available
                - driver_id
                - registration
                - price
                - status
              properties:
                date:
                  type: string
                  description: Date the ride will be taken.
                time:
                  type: string
                  description: Time the ride will start.
                pickup:
                  type: string
                  description: Place the ride will be taken from.
                dropoff:
                  type: string
                  description: Destination of the ride.
                capacity:
                  type: string
                  description: The car's passenger capacity.
                seats_available:
                  type: string
                  description: The seats that are still on offer.
                driver_id:
                  type: string
                  description: Unique identifier of the driver.
                registration:
                  type: string
                  description: The car's licence plate.
                price:
                  type: string
                  description: The price of the ride.
                status:
                  type: string
                  description: The status of the ride.
        responses:
          201:
            description: Ride creation successful
            schema:
              $ref: '#/definitions/Ride'
        """
        self.ride.abort_if_ride_offer_doesnt_exist(ride_id)
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return self.ride.edit(
                    args['date'], 
                    args['time'], 
                    args['pickup'], 
                    args['dropoff'], 
                    args['capacity'], 
                    args['available_seats'], 
                    args['driver_id'], 
                    args['registration'], 
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
          200:
            description: Fetch successfull
          404:
            description: There ride offer does not exist
        """
        request = self.ride.abort_if_ride_offer_doesnt_exist(ride_id)
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
          200:
            description: Ride successfully deleted
          404:
            description: The ride offer does not exist
        """
        self.ride.abort_if_ride_offer_doesnt_exist(ride_id)
        return self.ride.delete(ride_id)

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
