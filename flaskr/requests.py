from flask_restful import abort
from random import randint


class Request:
    def __init__(self, requestor_id, requestor_name, request_status='Pending'):
        self.requestor_id = requestor_id
        self.requestor_name = requestor_name
        self.request_status = request_status

    def accept(self):
        self.request_status = 'Accepted'

    def decline(self):
        self.request_status = 'Declined'

    def json_dump(self):
        request = dict(
            requestor_id=self.requestor_id,
            requestor_name=self.requestor_name,
            request_status=self.request_status,
        )
        return request
