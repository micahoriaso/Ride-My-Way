from datetime import datetime
from flask import make_response, abort, jsonify, request, Blueprint

bp = Blueprint('rides', __name__)

rides = {
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

# Create a handler for our read (GET) rides

def read():
    """
    This function responds to a request for /api/v1/rides
    with the complete list of ride offers
    """
    # Create the list of ride offers from our data
    return make_response(
        jsonify(
            [rides[key] for key in sorted(rides.keys())]
        ), 200)

@bp.route('/api/v1/rides/', methods=['GET'])
def get_rides():
    return read()
