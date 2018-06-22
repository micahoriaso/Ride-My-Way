from flask import request

from flask_restful import Resource

from flaskr.rides import Ride, Rides

class RidesResource(Resource):
    def __init__(self):
        self.rides = Rides()
        
    # GET method for ride offers list
    def get(self):
        return self.rides.browse(), 200
    
    # POST method for new ride offer
    def post(self):
        ride = request.get_json(force=True)
        self.rides.add(ride)
        response = ride
        return {'status': 'success', 'data': response}, 201

    # PUT method for editing a ride offer
    def put(self, ride_id):
        ride = request.get_json(force=True)
        self.rides.edit(ride_id, ride)
        response = ride
        return {'status': 'success', 'data': response}, 200

    # DELETE method for editing a ride offer
    def delete(self, ride_id):
        return self.rides.delete(ride_id), 200


class RideResource(Resource):
    # GET method for a ride offer
    def get(self, ride_id):
        rides = Rides()
        return rides.read(ride_id), 200


