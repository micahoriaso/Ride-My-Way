import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flaskr.db import connectDB


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

        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        super(RideListResource, self).__init__()

        # POST method for new ride request
    def post(self):
        args = self.reqparse.parse_args()
        try:
            self.cursor.execute(
                """INSERT INTO ride (
                    date,
                    time,
                    pickup, 
                    dropoff,
                    capacity,
                    seats_available,
                    driver_id,
                    registration,
                    price,
                    status
                    ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (
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
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': args}, 201


class RideResource(Resource):
    pass


rides_v2_bp = Blueprint('resourcesV2.rides', __name__)
api = Api(rides_v2_bp)
api.add_resource(
    RideResource, 
    '/api/v2/rides/<ride_id>',
    '/api/v2/rides/<ride_id>/'
)
api.add_resource(
    RideListResource, 
    '/api/v2/rides',
    '/api/v2/rides/',
    '/api/v2/rides/<ride_id>',
    '/api/v2/rides/<ride_id>/'
    )