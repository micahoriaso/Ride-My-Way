from flask import request, json
from flask_restful import Resource
from random import randint

from flaskr.rides import Ride, Rides
from flaskr.requests import Request

class RequestResource(Resource):
    
    def __init__(self):
        self.rides = Rides()

    # GET method for ride offers list
    def get(self, ride_id):
        ride = self.rides.get_ride(ride_id)
        response = ride.get_request()
        return {"status": "success", "data": response}, 200
    
    def post(self, ride_id):
        ride = self.rides.get_ride(ride_id)
        ride_request = request.get_json(force=True)
        ride.add_request(ride_request)
        response = ride.json_dump()
        return {"status": "success", "data": response}, 201