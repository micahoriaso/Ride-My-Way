from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

requests = []


class RequestListResource(Resource):
    pass

class RequestResource(Resource):
    pass


requests_v2_bp = Blueprint('resourcesV2.requests', __name__)
api = Api(requests_v2_bp)
api.add_resource(
    RequestResource, 
    '/api/v2/rides/<ride_id>/requests/<request_id>',
    '/api/v2/rides/<ride_id>/requests/<request_id>/'
)
api.add_resource(
    RequestListResource, 
    '/api/v2/rides/<ride_id>/requests',
    '/api/v2/rides/<ride_id>/requests/',
    '/api/v2/rides/<ride_id>/requests/<request_id>',
    '/api/v2/rides/<ride_id>/requests/<request_id>/'
    )
