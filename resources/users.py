import psycopg2
import psycopg2.extras


from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import connectDB

from resources.helpers import match_email, strip_whitespace


class UserListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='Please enter firstname', location='json'
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
            'phone_number', type=str, default='', location='json'
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
        """
        Endpoint for user sign up
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: User
              required:
                - firstname
                - lastname
                - email
                - password
                - confirm_password
              properties:
                firstname:
                  type: string
                  description: The user's firstname.
                lastname:
                  type: string
                  description: The user's lastname.
                email:
                  type: string
                  description: The user's email.
                password:
                  type: string
                  description: The user's password.
                confirm_password:
                  type: string
                  description: Confirmation of the password entered.
        responses:
          201:
            description: Account creation successful
          202:
            description: Password is too short. At least 8 characters required
            schema:
              $ref: '#/definitions/User'
        """
  
        args = self.reqparse.parse_args()
        self.abort_if_email_is_already_used(args['email'])
        if match_email(args['email']):
            if args['password'] == args['confirm_password']:
                if len(args['password']) >= 8:
                    try:
                        self.cursor.execute(
                            """INSERT INTO app_user (
                                firstname, 
                                lastname, 
                                fullname, 
                                email,
                                phone_number,
                                password,
                                car_registration
                                )
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                            (
                                args['firstname'],
                                args['lastname'],
                                '{} {}'.format(
                                    args['firstname'], args['lastname']
                                    ),
                                args['email'],
                                args['phone_number'],
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
                        return {'status': 'failed', 'message': error}, 500
                    return {'status': 'success', 'message': 'Account creation successful'}, 201
                return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 202
            return {'status': 'failed', 'message': 'Password and confirm password do not match, try again'}, 202
        return {'status': 'failed', 'message': 'Invalid email address, try again'}, 202

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
        """
        Endpoint for user log in
        ---
        tags:
          - User
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Login
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: The user's email.
                password:
                  type: string
                  description: The user's password.
        responses:
          200:
            description: Login successful
          202:
            description: Invalid email/password combination
          404:
            description: The user with email string does not exist
            schema:
              $ref: '#/definitions/Login'
              """
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
                return {'status': 'success', 'message': 'Login successful'}, 200
            return {'status': 'failed', 'message': 'Invalid email/password combination'}, 202
        else:
            abort(404, message='The user with email {} does not exist'.format(
                args['email']))


class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='Please enter firstname', location='json'
        )
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='Please enter lastname', location='json'
        )
        self.reqparse.add_argument(
            'car_registration', location='json'
        )
        self.reqparse.add_argument(
            'phone_number', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )

        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        super(UserResource, self).__init__()

    # DELETE method for deleting a user
    def delete(self, user_id):
        """
        Endpoint for deleting a user's profile
        ---
        tags:
          - User
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          200:
            description: User successfully deleted
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        self.abort_if_user_doesnt_exist(user_id)
        try:
            self.cursor.execute('DELETE FROM app_user WHERE id = %s ;',
                                ([user_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'message': error}, 200
        return {'status': 'success', 'message': 'User successfully deleted'}, 200

    # GET method for a user
    def get(self, user_id):
        """
        Endpoint for viewing a user's details
        ---
        tags:
          - User
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          200:
            description: Fetch successfull
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        request = self.abort_if_user_doesnt_exist(user_id)
        return {'status': 'success', 'message': 'Fetch successful', 'data': request}

    # PUT method for updating user
    def put(self, user_id):
        """
        Endpoint for user profile update
        ---
        tags:
          - User
        parameters:
          - name: user_id
            in: path
            required: true
          - name: body
            in: body
            required: true
            schema:
              id: UserUpdate
              required:
                - firstname
                - lastname
                - password
                - car_registration
                - phone_number
              properties:
                firstname:
                  type: string
                  description: The user's firstname.
                lastname:
                  type: string
                  description: The user's lastname.
                password:
                  type: string
                  description: The user's password.
                car_registration:
                  type: string
                  description: The user's car licence plate.
                phone_number:
                  type: string
                  description: The user's phone number.
        responses:
          200:
            description: Update successful
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        args = self.reqparse.parse_args()
        self.abort_if_user_doesnt_exist(user_id)
        if len(args['password']) >= 8:
            try:
                self.cursor.execute(
                    """UPDATE app_user SET
                        firstname = %s, 
                        lastname = %s, 
                        fullname = %s, 
                        phone_number = %s, 
                        password = %s, 
                        car_registration = %s 
                    WHERE id = %s;""",
                    (
                        args['firstname'],
                        args['lastname'],
                        '{} {}'.format(
                            args['firstname'], args['lastname']
                        ),
                        args['phone_number'],
                        generate_password_hash(
                            args['password'],
                            method='sha256'
                        ),
                        args['car_registration'],
                        int(user_id)
                    )
                )
                self.connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                self.connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            return {'status': 'success', 'data': args}, 200
        return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 202

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


users_bp = Blueprint('resources.users', __name__)
api = Api(users_bp)

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
