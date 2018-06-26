from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

rides = []

class RideListResource(Resource):
    pass


class RideResource(Resource):
    pass


rides_v2_bp = Blueprint('resourcesV2.rides', __name__)
api = Api(rides_v2_bp)
api.add_resource(
    RideResource, 
    '/api/v2/rides/<ride_id>',
    '/api/v2/rides/<ride_id>/'
)
api.add_resource(
    RideListResource, 
    '/api/v2/rides',
    '/api/v2/rides/',
    '/api/v2/rides/<ride_id>',
    '/api/v2/rides/<ride_id>/'
    )
