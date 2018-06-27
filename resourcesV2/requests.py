import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flaskr.db import connectDB




class RequestListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'requestor_id', type=int, required=True, help='Please enter requestor', location='json'
        )
        self.reqparse.add_argument(
            'request_status', type=str, location='json', default='Pending'
        )
        self.reqparse.add_argument(
            'ride_id', type=int, location='json'
        )
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        super(RequestListResource, self).__init__()

    # POST method for new ride request
    def post(self, ride_id):
        args = self.reqparse.parse_args()
        self.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            self.cursor.execute(
                """INSERT INTO ride_request (ride_id, requestor_id, request_status) 
                VALUES (%s, %s, %s);""",
                (int(ride_id), args['requestor_id'], args['request_status']))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': args}, 201

    def abort_if_ride_offer_doesnt_exist(self, ride_id):
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

class RequestResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'request_status', type=str, location='json', default='Pending'
        )

        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        super(RequestResource, self).__init__()

    # GET method for a ride request
    def get(self, ride_id, request_id):
        request = self.abort_if_ride_request_doesnt_exist(request_id)
        return {'data': request}

    def abort_if_ride_request_doesnt_exist(self, request_id):
        try:
            self.cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(404, message='The ride request with id {} does not exist'.format(request_id))
        return results


requests_v2_bp = Blueprint('resourcesV2.requests', __name__)
api = Api(requests_v2_bp)
api.add_resource(
    RequestResource, 
    '/api/v2/rides/<ride_id>/requests/<request_id>',
    '/api/v2/rides/<ride_id>/requests/<request_id>/'
)
api.add_resource(
    RequestListResource, 
    '/api/v2/rides/<ride_id>/requests',
    '/api/v2/rides/<ride_id>/requests/',
    '/api/v2/rides/<ride_id>/requests/<request_id>',
    '/api/v2/rides/<ride_id>/requests/<request_id>/'
    )
