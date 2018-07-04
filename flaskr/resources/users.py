import psycopg2
import psycopg2.extras


from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from flask_jwt_extended import jwt_required

from flaskr.resources.helpers import match_email, check_for_empty_fields
from flaskr.models.user import User


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
            'car_registration', type=str, default=None, location='json'
        )
        self.reqparse.add_argument(
            'phone_number', type=str, default=None, location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )
        self.reqparse.add_argument(
            'confirm_password', type=str, required=True, help='Please enter the confirm password', location='json'
        )
        

        super(UserListResource, self).__init__()

    # POST method for new user
    def post(self):
        """
        Endpoint for user sign up
        ---
        tags:
          - User
        security:
          - Bearer: []  
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
          500:
            description: Internal server error
          201:
            description: Account creation successful
          202:
            description: Password is too short. At least 8 characters required
            schema:
              $ref: '#/definitions/User'
        """
  
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        if match_email(args['email']):
            if args['password'] == args['confirm_password']:
                if len(args['password']) >= 8:
                    user = User(args['firstname'],
                                args['lastname'], args['email'],
                                args['password'], args['phone_number'],
                                args['car_registration'])
                    return user.add()
                return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 202
            return {'status': 'failed', 'message': 'Password and confirm password do not match, try again'}, 202
        return {'status': 'failed', 'message': 'Invalid email address, try again'}, 202

class LoginResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email', type=str, required=True, help='Please enter email', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location='json'
        )
        

        super(LoginResource, self).__init__()

    def post(self):
        """
        Endpoint for user log in
        ---
        tags:
          - User
        security:
          - Bearer: []  
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
          500:
            description: Internal server error
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
        check_for_empty_fields(args)
        return User.login(args['email'], args['password'])


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

        
        super(UserResource, self).__init__()

    # DELETE method for deleting a user
    @jwt_required
    def delete(self, user_id):
        """
        Endpoint for deleting a user's profile
        ---
        tags:
          - User
        security:
          - Bearer: []  
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: User successfully deleted
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        return User.delete(user_id)

    # GET method for a user
    @jwt_required
    def get(self, user_id):
        """
        Endpoint for viewing a user's details
        ---
        tags:
          - User
        security:
          - Bearer: []  
        parameters:
          - name: user_id
            in: path
            required: true
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        return User.read(user_id)

    # PUT method for updating user
    @jwt_required
    def put(self, user_id):
        """
        Endpoint for user profile update
        ---
        tags:
          - User
        security:
          - Bearer: []  
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
          500:
            description: Internal server error
          200:
            description: Update successful
          404:
            description: The user does not exist
            schema:
              $ref: '#/definitions/UserUpdate'
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        if len(args['password']) >= 8:
            return User.edit(
                user_id,
                args['firstname'],
                args['lastname'],
                args['password'], args['phone_number'],
                args['car_registration']
            )
        return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 202



users_bp = Blueprint('resources.users', __name__)
api = Api(users_bp)

api.add_resource(
    UserListResource,
    '/api/v2/auth/signup'
)
api.add_resource(
    LoginResource,
    '/api/v2/auth/login'
)
api.add_resource(
    UserResource,
    '/api/v2/users/<user_id>'
)
