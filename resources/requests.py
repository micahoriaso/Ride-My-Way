from flask import request

from flask_restful import Resource

from flaskr.requests import Request , RequestList


class RequestListResource(Resource):
    def __init__(self):
        self.requests = RequestList()

    # GET method for ride offers list
    def get(self, ride_id):
        response = self.requests.browse(ride_id)
        return {'status': 'success', 'data': response}, 200

    # POST method for new ride offer
    def post(self, ride_id):
        ride_request = request.get_json(force=True)
        response = self.requests.add(ride_id, ride_request)
        return {'status': 'success', 'data': response}, 201

    # PUT method for editing a ride offer
    def put(self, ride_id, request_id):
        ride_request = request.get_json(force=True)
        response = self.requests.edit(ride_id, request_id, ride_request)
        return {'status': 'success', 'data': response}, 200

    # DELETE method for editing a ride offer
    def delete(self, ride_id, request_id):
        response = self.requests.delete(ride_id, request_id)
        return {'status': 'success', 'data': response}, 200


class RequestResource(Resource):
    # GET method for a ride offer
    def get(self, ride_id, request_id):
        requests = RequestList()
        return requests.read(request_id), 200
