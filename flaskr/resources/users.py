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
            'firstname', type=str, required=True, help='Please enter firstname', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='Please enter lastname', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email', type=str, required=True, help='Please enter email', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'car_registration', type=str, default=None, location=['form', 'json']
        )
        self.reqparse.add_argument(
            'phone_number', type=str, default=None, location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location=['form', 'json']
        )
        self.reqparse.add_argument(
            'confirm_password', type=str, required=True, help='Please enter the confirm password', location=['form', 'json']
        )
        

        super(UserListResource, self).__init__()

    # POST method for new user
    def post(self):
        """
        Endpoint for user sign up
        ---
        tags:
          - User
        parameters:
          - name: firstname
            in: formData
            required: true
            description: The user's firstname.
            type: string
          - name: lastname
            in: formData
            required: true
            description: The user's lastname.
            type: string
          - name: email
            in: formData
            required: true
            description: The user's email.
            type: string
          - name: password
            in: formData
            required: true
            description: The user's password.
            type: string
            format: password
          - name: confirm_password
            in: formData
            required: true
            description: Confirmation of the password entered.
            type: string
            format: password
        responses:
          500:
            description: Internal server error
          201:
            description: Account creation successful
          202:
            description: Password is too short. At least 8 characters required
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
            'email', type=str, required=True, help='Please enter email', location=['form','json']
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location=['form','json']
        )
        

        super(LoginResource, self).__init__()

    # Method for loggin in a user
    def post(self):
        """
        Endpoint for user log in
        ---
        tags:
          - User
        security:
          - Bearer: []  
        parameters:
          - name: email
            in: formData
            required: true
            description: The user's email.
            type: string
          - name: password
            in: formData
            required: true
            description: The user's password.
            type: string
            format: password
        responses:
          500:
            description: Internal server error
          200:
            description: Login successful
          202:
            description: Wrong password, please try again.
          404:
            description: The user with email string does not exist
        """
        args = self.reqparse.parse_args()
        check_for_empty_fields(args)
        if match_email(args['email']):
          return User.login(args['email'], args['password'])
        return {'status': 'failed', 'message': 'Invalid email address, try again'}, 202



class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True, help='Please enter firstname', location=['form','json']
        )
        self.reqparse.add_argument(
            'lastname', type=str, required=True, help='Please enter lastname', location=['form','json']
        )
        self.reqparse.add_argument(
            'car_registration', location=['form','json']
        )
        self.reqparse.add_argument(
            'phone_number', location=['form','json']
        )
        self.reqparse.add_argument(
            'password', type=str, required=True, help='Please enter password', location=['form','json']
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
            type: integer
        responses:
          500:
            description: Internal server error
          200:
            description: User successfully deleted
          404:
            description: The user does not exist
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
            type: integer
        responses:
          500:
            description: Internal server error
          200:
            description: Fetch successfull
          404:
            description: The user does not exist
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
            type: integer
          - name: firstname
            in: formData
            required: true
            description: The user's firstname.
            type: string
          - name: lastname
            in: formData
            required: true
            description: The user's lastname.
            type: string
          - name: password
            in: formData
            required: true
            description: The user's password.
            type: string
            format: password
          - name: car_registration
            in: formData
            description: The user's car licence plate.
            type: string
          - name: phone_number
            in: formData
            description: The user's phone number.
            type: string
        responses:
          500:
            description: Internal server error
          200:
            description: Update successful
          404:
            description: The user does not exist
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
