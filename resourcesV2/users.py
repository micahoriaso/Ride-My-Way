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
            'password', type=str, location='json'
        )

        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        super(UserResource, self).__init__()

    # GET method for a user
    def get(self, user_id):
        request = self.abort_if_user_doesnt_exist(user_id)
        return {'data': request}

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
            abort(404, message='The user with id {} does not exist'.format(user_id))
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

