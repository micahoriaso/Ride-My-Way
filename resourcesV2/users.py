import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import connectDB

class UserListResource(Resource):
    pass


class LoginResource(Resource):
    pass


class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='Please enter firsname', location='json'
        )
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='Please enter lastname', location='json'
        )
        self.reqparse.add_argument(
            'car_registration', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        super(UserResource, self).__init__()

    # PUT method for updating user
    def put(self, user_id):
        args = self.reqparse.parse_args()
        self.abort_if_user_doesnt_exist(user_id)
        try:
            self.cursor.execute(
                """UPDATE app_user SET
                    firstname = %s, 
                    lastname = %s, 
                    fullname = %s, 
                    car_registration = %s 
                WHERE id = %s;""",
                (
                    args['firstname'],
                    args['lastname'],
                    '{} {}'.format(
                        args['firstname'], args['lastname']
                    ),
                    args['car_registration'],
                    int(user_id)
                )
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': args}, 201

    def abort_if_user_doesnt_exist(self, user_id):
        try:
            self.cursor.execute('SELECT * FROM app_user WHERE id = %s ;',
                                ([user_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(400, message='The user {} does not exist'.format(user_id))
        return results


users_v2_bp = Blueprint('resourcesV2.users', __name__)
api = Api(users_v2_bp)
api.add_resource(
    UserListResource, 
    '/api/v2/auth/signup',
    '/api/v2/auth/signup/'
    )
api.add_resource(
    LoginResource, 
    '/api/v2/auth/login',
    '/api/v2/auth/login'
    )
api.add_resource(
    UserResource, 
    '/api/v2/users/<user_id>',
    '/api/v2/users/<user_id>'
    )

