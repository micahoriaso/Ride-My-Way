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

    # GET method for ride list
    def get(self):
        try:
            self.cursor.execute('SELECT * FROM ride;')
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_list = self.cursor.fetchall()
        if len(ride_list) == 0:
            return {'status': 'success', 'message': 'There are no rides offers yet'}
        else:
            return {'status': 'success', 'data': ride_list}

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
        super(RideResource, self).__init__()


    # PUT method for editing a ride request
    def put(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        args = self.reqparse.parse_args()
        try:
            self.cursor.execute(
                """UPDATE ride SET 
                    date = %s,
                    time = %s,
                    pickup = %s,
                    dropoff = %s,
                    capacity = %s,
                    seats_available = %s,
                    driver_id = %s,
                    registration = %s,
                    price = %s,
                    status = %s
                 WHERE id = %s;""",
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
                    args['status'], 
                    ride_id
                )
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 200
        return {'status': 'success', 'data': 'Ride request successfully updated'}, 200

        
    # GET method for a ride request
    def get(self, ride_id):
        request = self.abort_if_ride_doesnt_exist(ride_id)
        return {'data': request}


    # DELETE method for deleting a ride request
    def delete(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        try:
            self.cursor.execute('DELETE FROM ride WHERE id = %s ;',
                                ([ride_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 200
        self.delete_this_rides_requests(ride_id)
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    def delete_this_rides_requests(self, ride_id):
        try:
            self.cursor.execute('DELETE FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 200
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    def abort_if_ride_doesnt_exist(self, ride_id):
            try:
                self.cursor.execute('SELECT * FROM ride WHERE id = %s ;',
                                    ([ride_id]))
            except (Exception, psycopg2.DatabaseError) as error:
                self.connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            results = self.cursor.fetchone()
            if results is None:
                abort(404, message='The ride with id {} does not exist'.format(ride_id))
            return results

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
