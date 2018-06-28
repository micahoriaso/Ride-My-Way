from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

rides = []

class RideListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, required=True, help='Please enter dropoff', location='json'
        )
        self.reqparse.add_argument(
            'pickup', type=str, required=True, help='Please enter pickup', location='json'
        )
        self.reqparse.add_argument(
            'time', type=str, required=True, help='Please enter time', location='json'
        )
        self.reqparse.add_argument(
            'price', type=float, required=True, help='Please enter price', location='json'
        )
        self.reqparse.add_argument(
            'date', type=str, required=True, help='Please enter the date', location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=int, required=True, help='Please enter the vehicle capacity', location='json'
        )
        self.reqparse.add_argument(
            'available_seats', type=int, required=True, help='Please enter the available seats', location='json'
        )
        self.reqparse.add_argument(
            'driver', type=str, required=True, help='Please enter the driver', location='json'
        )
        self.reqparse.add_argument(
            'car', type=str, required=True, help='Please enter the car', location='json'
        )
        self.reqparse.add_argument(
            'registration', type=str, required=True, help='Please enter the registration', location='json'
        )
        self.reqparse.add_argument(
            'ride_status', type=str, required=False, help='Please enter the ride status', default='In Offer', location='json'
        )

        super (RideListResource, self).__init__()
        
    # GET method for ride offers list
    def get(self):
        if len(rides) == 0:
            return {'status': 'success', 'message': 'No available rides yet'}
        else:
            return {'status': 'success', 'data': rides}

    
    # POST method for new ride offer
    def post(self):
        args = self.reqparse.parse_args()
        ride = {
            'id': len(rides) + 1,
            'dropoff': args['dropoff'],
            'pickup': args['pickup'],
            'time': args['time'],
            'price': args['price'],
            'date': args['date'],
            'capacity': args['capacity'],
            'available_seats': args['available_seats'],
            'driver': args['driver'],
            'car': args['car'],
            'registration': args['registration'],
            'ride_status': args['ride_status']
        }
        rides.append(ride)
        return {'status': 'success', 'data': ride}, 201


class RideResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'dropoff', type=str, location='json'
        )
        self.reqparse.add_argument(
            'pickup', type=str, location='json'
        )
        self.reqparse.add_argument(
            'time', type=str, location='json'
        )
        self.reqparse.add_argument(
            'price', type=float, location='json'
        )
        self.reqparse.add_argument(
            'date', type=str, location='json'
        )
        self.reqparse.add_argument(
            'capacity', type=int, location='json'
        )
        self.reqparse.add_argument(
            'available_seats', type=int, location='json'
        )
        self.reqparse.add_argument(
            'driver', type=str, location='json'
        )
        self.reqparse.add_argument(
            'car', type=str, location='json'
        )
        self.reqparse.add_argument(
            'registration', type=str, location='json'
        )
        self.reqparse.add_argument(
            'ride_status', type=str, location='json'
        )

        super(RideResource, self).__init__()

    # GET method for a ride offer
    def get(self, ride_id):
        ride = self.abort_if_ride_doesnt_exist(ride_id)
        return {'ride': ride[0]}

    # PUT method for editing a ride offer
    def put(self, ride_id):
        ride = self.abort_if_ride_doesnt_exist(ride_id)
        ride = ride[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                ride[k] = v
        return {'status': 'success', 'data': ride}, 200

    # DELETE method for deleting a ride offer
    def delete(self, ride_id):
        ride = self.abort_if_ride_doesnt_exist(ride_id)
        rides.remove(ride[0])
        return {'status': 'success', 'data': 'Ride successfully deleted'}, 200

    def abort_if_ride_doesnt_exist(self, ride_id):
        ride = [ride for ride in rides if ride['id'] == int(ride_id)]
        if len(ride) == 0:
            abort(404, message='The ride offer {} does not exist'.format(ride_id))
        return ride


rides_bp = Blueprint('resourcesV1.rides', __name__)
api = Api(rides_bp)
api.add_resource(
    RideResource, 
    '/api/v1/rides/<ride_id>',
    '/api/v1/rides/<ride_id>/'
)
api.add_resource(
    RideListResource, 
    '/api/v1/rides',
    '/api/v1/rides/',
    '/api/v1/rides/<ride_id>',
    '/api/v1/rides/<ride_id>/'
    )
