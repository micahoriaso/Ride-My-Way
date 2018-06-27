import psycopg2
import psycopg2.extras

from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import connectDB


class UserListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='Please enter firsname', location='json'
        )
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='Please enter lastname', location='json'
        )
        self.reqparse.add_argument(
            'email', type=str, required=True, help='Please enter email', location='json'
        )
        self.reqparse.add_argument(
            'car_registration', type=str, default='', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )
        self.reqparse.add_argument(
            'confirm_password', type=str, required=True, help='Please enter the confirm password', location='json'
        )
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

        super(UserListResource, self).__init__()

        # POST method for new user
    def post(self):
        args = self.reqparse.parse_args()
        self.abort_if_email_is_already_used(args['email'])
        if args['password'] == args['confirm_password']:
            if len(args['password']) >= 8:
                try:
                    self.cursor.execute(
                        """INSERT INTO app_user (
                            firstname, 
                            lastname, 
                            fullname, 
                            email,
                            password,
                            car_registration
                            )
                        VALUES (%s, %s, %s, %s, %s, %s);""",
                        (
                            args['firstname'],
                            args['lastname'],
                            '{} {}'.format(
                                args['firstname'], args['lastname']
                                ),
                            args['email'],
                            generate_password_hash(
                                args['password'], 
                                method='sha256'
                                ),
                            args['car_registration']
                        )
                    )
                    self.connection.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    self.connection.rollback()
                    return {'status': 'failed', 'data': error}, 500
                return {'status': 'success', 'data': args}, 201
            return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 400
        return {'status': 'failed', 'message': 'Password and confirm password do not match, try again'}, 400

    def abort_if_email_is_already_used(self, email):
        try:
            self.cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is not None:
            abort(400, message='The email {} is already taken'.format(email))
        return results


class LoginResource(Resource):
    pass


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

