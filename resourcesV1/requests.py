from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal, abort, Api

requests = []

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
        super(RequestListResource, self).__init__()

    # GET method for ride requests list
    def get(self, ride_id):
        ride_offer_request = [
            request for request in requests if request['ride_id'] == int(ride_id)
            ]
        if len(ride_offer_request) == 0:
            return {'status': 'success', 'message': 'No requests available for this ride yet'}
        else:
            return {'status': 'success', 'data': ride_offer_request}

    # POST method for new ride offer
    def post(self, ride_id):
        args = self.reqparse.parse_args()
        request = {
            'id': len(requests) + 1,
            'requestor_id': args['requestor_id'],
            'ride_id': int(ride_id),
            'request_status': args['request_status']
        }
        requests.append(request)
        return {'status': 'success', 'data': request}, 201

class RequestResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'request_status', type=str, location='json', default='Pending'
        )
        super(RequestResource, self).__init__()

    # GET method for a ride request
    def get(self, ride_id, request_id):
        request = self.abort_if_ride_request_doesnt_exist(request_id)
        return {'data': request[0]}

    # PUT method for editing a ride request
    def put(self, ride_id, request_id):
        request = self.abort_if_ride_request_doesnt_exist(request_id)
        request = request[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                request[k] = v
        return {'status': 'success', 'data': request}, 200

    # DELETE method for deleting a ride request
    def delete(self, ride_id, request_id):
        request = self.abort_if_ride_request_doesnt_exist(request_id)
        requests.remove(request[0])
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    def abort_if_ride_request_doesnt_exist(self, request_id):
            request = [request for request in requests if request['id'] == int(request_id)]
            if len(request) == 0:
                abort(404, message='The request {} does not exist'.format(request_id))
            return request


requests_v1_bp = Blueprint('resourcesV1.requests', __name__)
api = Api(requests_v1_bp)
api.add_resource(
    RequestResource, 
    '/api/v1/rides/<ride_id>/requests/<request_id>', 
    '/api/v1/rides/<ride_id>/requests/<request_id>/'
)
api.add_resource(
    RequestListResource, 
    '/api/v1/rides/<ride_id>/requests',
    '/api/v1/rides/<ride_id>/requests/',
    '/api/v1/rides/<ride_id>/requests/<request_id>',
    '/api/v1/rides/<ride_id>/requests/<request_id>/'
    )
