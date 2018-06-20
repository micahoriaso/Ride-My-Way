from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource

RIDES = {
    "1": {
        "id": 1,
        "date": "12-06-2018",
        "time": "11:00",
        "pickup": "Nyayo Stadium",
        "dropoff": "Belle Vue",
        "price": "100",
        "capacity": "3",
        "available_seats": "1",
        "driver": "Farrell",
        "car": "Mazda MX5",
        "registration": "KAA 987I",
    },
    "2": {
        "id": 2,
        "date": "12-06-2018",
        "time": "13:00",
        "pickup": "Belle Vue",
        "dropoff": "Nyayo Stadium",
        "price": "100",
        "capacity": "3",
        "available_seats": "3",
        "driver": "Farrell",
        "car": "Mazda MX5",
        "registration": "KAA 987I",
    },
    "3": {
        "id": 3,
        "date": "14-06-2018",
        "time": "08:00",
        "pickup": "Ongata Rongai",
        "dropoff": "T Mall",
        "price": "200",
        "capacity": "3",
        "available_seats": "3",
        "driver": "Kent",
        "car": "Honda Civic",
        "registration": "KAG 987I",
    }
}


def abort_if_ride_doesnt_exist(ride_id):
    if ride_id not in RIDES:
        abort(404, message="The ride offer {} doesn't exist".format(ride_id))


# Create a handler for our read (GET) rides

def read():
    """
    This function responds to a request for /api/v1/rides
    with the complete list of ride offers
    """
    # Create the list of ride offers from our data
    return [RIDES[key] for key in sorted(RIDES.keys())]

def read_one(key):
    """
    This function responds to a request for /api/v1/rides/<ride_id>
    with a ride offer
    """
    # Create the list of ride offers from our data
    return RIDES[key]

class RideList(Resource):
    # GET method for ride offers list
    def get(self):
        return read(), 200

class Ride(Resource):
    # GET method for a ride offer
    def get(self, ride_id):
        abort_if_ride_doesnt_exist(ride_id)
        return read_one(ride_id), 200
