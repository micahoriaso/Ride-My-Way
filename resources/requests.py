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

    # GET method for ride requests list
    def get(self, ride_id):
        """
        Endpoint for getting a list of all ride requests for a particular ride
        ---
        tags:
          - Ride request
        parameters:
          - name: ride_id
            in: path
            required: true
        responses:
          200:
            description: Fetch successfull
          404:
            description: No requests made for this ride yet'
        """
        self.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            self.cursor.execute('SELECT id, ride_id, requestor_id, request_status FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_offer_request = self.cursor.fetchall()
        if len(ride_offer_request) == 0:
            return {'status': 'success', 'message': 'No requests available for this ride yet'}
        else:
            return {'status': 'success', 'message': 'Fetch successful','data': ride_offer_request}

    # POST method for new ride request
    def post(self, ride_id):
        """
        Endpoint for creating a ride request
        ---
        tags:
          - Ride request
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: body
            in: body
            required: true
            schema:
              id: RideRequest
              required:
                - requestor_id
              properties:
                requestor_id:
                  type: integer
                  description: Unique identifier of the requestor.
                # request_status:
                #   type: string
                #   description: Current status of the request.
                # ride_id:
                #   type: string
                #   description: Unique identifier of the ride offer.
        responses:
          201:
            description: Ride successfully requested
            schema:
              $ref: '#/definitions/RideRequest'
        """
        args = self.reqparse.parse_args()
        self.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            self.cursor.execute(
                """INSERT INTO ride_request (ride_id, requestor_id, request_status) 
                VALUES (%s, %s, %s);""",
                (ride_id, args['requestor_id'], args['request_status']))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'message': 'Ride requested successfully' ,'data': args}, 201

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

    # DELETE method for deleting a ride request
    def delete(self, ride_id, request_id):
        """
        Endpoint for deleting a ride request
        ---
        tags:
          - Ride request
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: request_id
            in: path
            required: true
        responses:
          200:
            description: Ride request successfully deleted
          404:
            description: The ride request does not exist
        """
        RequestListResource().abort_if_ride_offer_doesnt_exist(ride_id)
        self.abort_if_ride_request_doesnt_exist(request_id)
        try:
            self.cursor.execute('DELETE FROM ride_request WHERE id = %s ;',
                                ([request_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 200

        return {'status': 'success', 'message': 'Ride request successfully deleted'}, 200

    # GET method for a ride request
    def get(self, ride_id, request_id):
        """
        Endpoint for getting a ride offer requests's details
        ---
        tags:
          - Ride request
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: request_id
            in: path
            required: true
        responses:
          200:
            description: Fetch successfull
          404:
            description: There ride offer or request does not exist
        """
        RequestListResource().abort_if_ride_offer_doesnt_exist(ride_id)
        request = self.abort_if_ride_request_doesnt_exist(request_id)
        return {'status': 'success', 'message': 'Fetch successful', 'data': request}
      
    
    def put(self, ride_id, request_id):
        # PUT method for editing a ride request
        """
        Endpoint for accepting/declining a ride request
        ---
        tags:
          - Ride request
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: request_id
            in: path
            required: true
          - name: body
            in: body
            required: true
            schema:
              id: UpdateRideRequest
              required:
                - requestor_id
              properties:
                request_status:
                  type: string
                  description: Current status of the request.
                  enum:
                    - "Pending"
                    - "Accepted"
                    - "Declined"
        responses:
          201:
            description: Ride request successfully updated
            schema:
              $ref: '#/definitions/UpdateRideRequest'
        """
        self.abort_if_ride_request_doesnt_exist(request_id)
        args = self.reqparse.parse_args()
        try:
            self.cursor.execute('UPDATE ride_request SET request_status = %s WHERE id = %s;',
                                (args['request_status'], request_id))

            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 200

        return {'status': 'success', 'data': 'Ride request successfully updated'}, 200

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


requests_bp = Blueprint('resourcesV2.requests', __name__)
api = Api(requests_bp)
api.add_resource(
    RequestResource, 
    '/api/v2/rides/<ride_id>/requests/<request_id>',
    '/api/v2/rides/<ride_id>/requests/<request_id>/'
)
api.add_resource(
    RequestListResource, 
    '/api/v2/rides/<ride_id>/requests',
    '/api/v2/rides/<ride_id>/requests/',
    )
