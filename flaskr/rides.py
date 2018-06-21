from datetime import datetime
from flask import request, json
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

def add_one(ride):
    """
    This function responds to a post request for /api/v1/rides/
    with a created success message
    """
    # Add a ride offer to the RIDES collection
    id = ride.get('id', None)
    date = ride.get('date', None)
    time = ride.get('time', None)
    pickup = ride.get('pickup', None)
    dropoff = ride.get('dropoff', None)
    price = ride.get('price', None)
    capacity = ride.get('capacity', None)
    available_seats = ride.get('available_seats', None)
    driver = ride.get('driver', None)
    car = ride.get('car', None)
    registration = ride.get('registration', None)
    
    # Does the ride exist already?
    if id not in RIDES and id is not None:
        RIDES[id] = {
            "id" : id,
            "date": date,
            "time": time,
            "pickup": pickup,
            "dropoff": dropoff,
            "price": price,
            "capacity": capacity,
            "available_seats": available_seats,
            "driver": driver,
            "car": car,
            "registration": registration,
        }
        return RIDES[id]

    else:
        abort(406, error ="Ride offer with id {} already exists".format(id))



class RideList(Resource):
    # GET method for ride offers list
    def get(self):
        return read(), 200

class Ride(Resource):
    # GET method for a ride offer
    def get(self, ride_id):
        abort_if_ride_doesnt_exist(ride_id)
        return read_one(ride_id), 200

    # POST method for a ride offer
    def post(self):
        json_data = request.get_json(force=True)
        return add_one(ride=json_data), 201
