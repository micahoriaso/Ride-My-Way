from flask_restful import abort
from random import randint

class Ride:
    def __init__(self, date, time, pickup, dropoff, price, capacity, available_seats, driver, car, registration):
        self.id = randint(1, 10)
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

    def json_dump(self):
        ride_meta = {}
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
        )
        ride_meta[self.id] = ride
        return ride_meta


class Rides:
    def __init__(self):
        self.RIDES = {
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
                "registration": "KAA 987I"
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
                "registration": "KAA 987I"
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
                "registration": "KAG 987I"
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
        return self.RIDES[ride_id]

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
            abort(406, error="Ride offer with id {} already exists".format(ride_id))

    def delete(self, ride_id):
        self.abort_if_ride_doesnt_exist(ride_id)
        del self.RIDES[ride_id]
        return self.RIDES

    def abort_if_ride_doesnt_exist(self, ride_id):
        if ride_id not in self.RIDES:
            abort(404, message="The ride offer {} doesn't exist".format(ride_id))
