import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import connectDB


class UserListResource(Resource):
    pass


class LoginResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email', type=str, required=True, help='Please enter email', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        super(LoginResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            self.cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([args['email']]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is not None:
            if results['email'] == args['email'] and check_password_hash(results['password'], args['password']):
                return {'status': 'success', 'data': 'Login successful'}, 200
            return {'status': 'failed', 'data': 'Invalid email/password combination'}, 400
        else:
            abort(404, message='The user with email {} does not exist'.format(
                args['email']))


class UserResource(Resource):
    pass


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

