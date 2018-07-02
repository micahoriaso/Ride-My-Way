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
            'requestor_id', type=int, required=True, help='Please enter requestor', location='json'
        )
        self.reqparse.add_argument(
            'request_status', type=str, location='json', default='Pending'
        )
        self.reqparse.add_argument(
            'ride_id', type=int, location='json'
        )
        self.ride_request = RideRequest()
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
          200:
            description: Fetch successfull
          404:
            description: No requests made for this ride yet'
        """
        self.ride_request.abort_if_ride_offer_doesnt_exist(ride_id)
        return self.ride_request.browse(ride_id)

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
        check_for_empty_fields(args)
        self.ride_request.abort_if_ride_offer_doesnt_exist(ride_id)
        return self.ride_request.add(ride_id, args['requestor_id'], args['request_status'])

class RequestResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'request_status', type=str, location='json', default='Pending'
        )
        self.ride_request = RideRequest()
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
          200:
            description: Ride request successfully deleted
          404:
            description: The ride request does not exist
        """
        self.ride_request.abort_if_ride_offer_doesnt_exist(ride_id)
        self.ride_request.abort_if_ride_request_doesnt_exist(request_id)
        return self.ride_request.delete(request_id)

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
          200:
            description: Fetch successfull
          404:
            description: There ride offer or request does not exist
        """
        self.ride_request.abort_if_ride_offer_doesnt_exist(ride_id)
        request = self.ride_request.read(request_id)
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
        self.ride_request.abort_if_ride_request_doesnt_exist(request_id)
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        return self.ride_request.edit(request_id, args['request_status'])


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
