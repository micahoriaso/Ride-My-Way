import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.models.request import RideRequest

from flaskr.resources.helpers import check_for_empty_fields




class RequestListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'requestor_id', type=int, required=True, help='Please enter requestor', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'request_status', type=str, location=['form', 'json'], default=RideRequest.STATUS_REQUESTED
        )
        self.reqparse.add_argument(
            'ride_id', type=int, location=['form', 'json']
        )
        super(RequestListResource, self).__init__()

    # GET method for ride requests list
    @jwt_required
    def get(self, ride_id):
        """
        Endpoint for getting a list of all ride requests for a particular ride
        ---
        tags:
          - Ride request
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
            description: No requests made for this ride yet'
        """
        return RideRequest.browse(ride_id)

    # POST method for new ride request
    @jwt_required
    def post(self, ride_id):
        """
        Endpoint for creating a ride request
        ---
        tags:
          - Ride request
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
            type: integer
            description: Unique identifier of the ride offer.
          - name: requestor_id
            in: formData
            required: true
            type: integer
            description: Unique identifier of the requestor.
        responses:
          500:
            description: Internal server error
          201:
            description: Ride successfully requested
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        ride_request = RideRequest(
            ride_id, args['requestor_id'], args['request_status'])
        return ride_request.add()

class RequestResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'request_status', type=str, location=['form', 'json'], default=RideRequest.STATUS_REQUESTED
        )
        super(RequestResource, self).__init__()

    # DELETE method for deleting a ride request
    @jwt_required
    def delete(self, ride_id, request_id):
        """
        Endpoint for deleting a ride request
        ---
        tags:
          - Ride request
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: request_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Ride request successfully deleted
          404:
            description: The ride request does not exist
        """
        return RideRequest.delete(ride_id, request_id)

    # GET method for a ride request
    @jwt_required
    def get(self, ride_id, request_id):
        """
        Endpoint for getting a ride offer requests's details
        ---
        tags:
          - Ride request
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
          - name: request_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: There ride offer or request does not exist
        """
        request = RideRequest.read(ride_id, request_id)
        return {'status': 'success', 'message': 'Fetch successful', 'data': request}
      
    
    @jwt_required
    def put(self, ride_id, request_id):
        # PUT method for editing a ride request
        """
        Endpoint for accepting/declining a ride request
        ---
        tags:
          - Ride request
        security:
          - Bearer: []  
        parameters:
          - name: ride_id
            in: path
            required: true
            type: integer
            description: Unique identifier of the ride offer.
          - name: request_id
            in: path
            required: true
            type: integer
            description: Unique identifier of the ride request.
          - name: request_status
            in: formData
            required: true
            type: string
            description: Current status of the request.
            enum:
              - "Accepted"
              - "Declined"
        responses:
          500:
            description: Internal server error
          201:
            description: Ride request successfully updated
            # schema:
            #   $ref: '#/definitions/UpdateRideRequest'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return RideRequest.edit(ride_id, request_id, args['request_status'])


requests_bp = Blueprint('resources.requests', __name__)
api = Api(requests_bp)
api.add_resource(
    RequestResource, 
    '/api/v2/rides/<ride_id>/requests/<request_id>'
)
api.add_resource(
    RequestListResource, 
    '/api/v2/rides/<ride_id>/requests'
    )
