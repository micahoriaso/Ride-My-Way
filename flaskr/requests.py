from flask_restful import abort
from random import randint

class Request:
    def __init__(
            self, id, ride_id, 
            requestor_id, requestor_name, 
            request_status='Pending'
        ):

        self.id = id
        self.ride_id = ride_id
        self.requestor_id = requestor_id
        self.requestor_name = requestor_name
        self.request_status = request_status

    def accept(self):
        self.request_status = 'Accepted'

    def decline(self):
        self.request_status = 'Declined'

    def json_dump(self):
        return {
            'id': self.id,
            'ride_id': self.ride_id,
            'requestor_id': self.requestor_id,
            'requestor_name': self.requestor_name,
            'request_status': self.request_status
        }

class RequestList:
    def __init__(self):
        self.REQUESTS = {
           '1': {
                'id': 1,
                'ride_id': 1,
                'requestor_id': 1,
                'requestor_name': 'Micah Oriaso',
                'request_status': 'Pending'
            },
            '2': {
                'id': 2,
                'ride_id': 1,
                'requestor_id': 2,
                'requestor_name': 'Charles Leclerc',
                'request_status': 'Accepted'
            },
            '3': {
                'id': 3,
                'ride_id': 2,
                'requestor_id': 3,
                'requestor_name': 'Pauline Were',
                'request_status': 'Accepted'
            }
        }

    def browse(self, ride_id):
        """
        This function responds to a request for /api/v1/requests
        with the complete list of ride offers
        """
        # Create the list of ride offers from our data
        ride_offer_request = []
        for item in self.REQUESTS:
            if self.REQUESTS[item]['ride_id'] == int(ride_id):
                ride_offer_request.append(self.REQUESTS[item])
        return ride_offer_request

    def read(self, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        return self.get_request(request_id).json_dump()

    def edit(self, ride_id, request_id, request):
        self.abort_if_request_doesnt_exist(request_id)
        self.REQUESTS[request_id] = request
        self.REQUESTS[str(request_id)]['ride_id'] = int(ride_id)
        return self.browse(ride_id)

    def add(self, ride_id, request):
        request_id = request.get('id', None)
        if str(request_id) not in self.REQUESTS:
            self.REQUESTS[str(request_id)] = request
            self.REQUESTS[str(request_id)]['ride_id'] = int(ride_id)
            return self.browse(ride_id)
        else:
            abort(406, error='Ride request with id {} already exists'.format(request_id))

    def delete(self, ride_id, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        del self.REQUESTS[request_id]
        return self.browse(ride_id)

    def get_request(self, request_id):
        self.abort_if_request_doesnt_exist(request_id)
        request = self.REQUESTS[request_id]
        return Request(
            request['id'],
            request['ride_id'],
            request['requestor_id'],
            request['requestor_name'],
            request['request_status'],
        )

    def abort_if_request_doesnt_exist(self, request_id):
        if str(request_id) not in self.REQUESTS:
            abort(404, message='The ride request {} does not exist'.format(request_id))
