from flask_restful import abort

from flaskr.requests import Request

class Ride:
    def __init__(
            self, id, date, time, pickup, 
            dropoff, price, capacity, 
            available_seats, driver, 
            car, registration, request = {}
        ):
        
        self.id = id
        self.date = date
        self.time = time
        self.pickup = pickup
        self.dropoff =dropoff
        self.price = price
        self.capacity = capacity
        self.available_seats = available_seats
        self.driver = driver
        self.car = car
        self.registration = registration
        self.request = request

    def add_request(self, request):
        requestor_id = request.get('requestor_id', None)
        requestor_name = request.get('requestor_name', None)

        if str(requestor_id) not in self.request:
            ride_request = Request(requestor_id, requestor_name)
            self.request[requestor_id] = ride_request.json_dump()
        else:
            abort(406, error='Ride request for user {} already exists'.format(
                requestor_id))


    def get_requests(self):
        return self.request

    def get_request(self, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        request = self.request[request_id]
        return Request(
            request['requestor_id'],
            request['requestor_name'],
            request['request_status'],
        )

    def read_request(self, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        return self.get_request(request_id).json_dump()

    def delete_request(self, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        del self.request[request_id]
        return self.request

    def abort_if_request_doesnt_exist(self, request_id):
        if request_id not in self.get_requests():
            abort(404, message='The ride request {} does not exist'.format(request_id))

    def json_dump(self):
        ride = dict(
            id=self.id,
            date=self.date,
            time=self.time,
            pickup=self.pickup,
            dropoff=self.dropoff,
            price=self.price,
            capacity=self.capacity,
            available_seats=self.available_seats,
            driver=self.driver,
            car=self.car,
            registration=self.registration,
            request=self.request
        )
        return ride

class Rides:
    def __init__(self):
        self.RIDES = {
            '1': {
                'id': 1,
                'date': '12-06-2018',
                'time': '11:00',
                'pickup': 'Nyayo Stadium',
                'dropoff': 'Belle Vue',
                'price': '100',
                'capacity': '3',
                'available_seats': '1',
                'driver': 'Farrell',
                'car': 'Mazda MX5',
                'registration': 'KAA 987I',
                'request': {}
            },
            '2': {
                'id': 2,
                'date': '12-06-2018',
                'time': '13:00',
                'pickup': 'Belle Vue',
                'dropoff': 'Nyayo Stadium',
                'price': '100',
                'capacity': '3',
                'available_seats': '3',
                'driver': 'Farrell',
                'car': 'Mazda MX5',
                'registration': 'KAA 987I',
                'request': {
                            '1': {
                                'requestor_id': 1,
                                'requestor_name': 'Cynthia West',
                                'request_status': 'Accepted',
                            },

                }
            },
            '3': {
                'id': 3,
                'date': '14-06-2018',
                'time': '08:00',
                'pickup': 'Ongata Rongai',
                'dropoff': 'T Mall',
                'price': '200',
                'capacity': '3',
                'available_seats': '3',
                'driver': 'Kent',
                'car': 'Honda Civic',
                'registration': 'KAG 987I',
                'request': {}
            }
        }

    def browse(self):
        """
        This function responds to a request for /api/v1/rides
        with the complete list of ride offers
        """
        # Create the list of ride offers from our data
        return [self.RIDES[key] for key in sorted(self.RIDES.keys())]

    def read(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        return self.get_ride(ride_id).json_dump()

    def edit(self, ride_id, ride):
        self.abort_if_ride_doesnt_exist(ride_id)
        self.RIDES[ride_id] = ride
        return self.RIDES[ride_id]

    def add(self, ride):
        ride_id = ride.get('id', None)
        if ride_id not in self.RIDES:
            self.RIDES[str(ride_id)] = ride
            return self.RIDES[ride_id]
        else:
            abort(406, error='Ride offer with id {} already exists'.format(ride_id))

    def delete(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        del self.RIDES[ride_id]
        return self.RIDES

    def get_ride(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        ride = self.RIDES[ride_id]
        return Ride(
            ride['id'],
            ride['date'],
            ride['time'],
            ride['pickup'],
            ride['dropoff'],
            ride['price'],
            ride['capacity'],
            ride['available_seats'],
            ride['driver'],
            ride['car'],
            ride['registration'],
            ride['request'],
        )

    def abort_if_ride_doesnt_exist(self, ride_id):
        if ride_id not in self.RIDES:
            abort(404, message='The ride offer {} does not exist'.format(ride_id))
