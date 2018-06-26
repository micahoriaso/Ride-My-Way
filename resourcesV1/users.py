from flask import Blueprint

from flask_restful import Resource, reqparse, fields, marshal, abort, Api

from werkzeug.security import generate_password_hash, check_password_hash

users = []

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

        super(UserListResource, self).__init__()
        
    # GET method for users list
    def get(self):
        if len(users) == 0:
            return {'status': 'success', 'message': 'No available users yet'}
        else:
            return {'status': 'success', 'data': users}

    
    # POST method for new user
    def post(self):
        args = self.reqparse.parse_args()
        user = {
            'id': len(users) + 1,
            'firstname': args['firstname'],
            'lastname': args['lastname'],
            'fullname': '{} {}'.format(args['firstname'], args['lastname']),
            'email': args['email'],
            'password': generate_password_hash(args['password'], method='sha256'),
            'car_registration': args['car_registration'],
        }
        self.abort_if_email_is_already_used(user['email'])
        if args['password'] == args['confirm_password']:
            if len(args['password']) >= 8:
                users.append(user)
                return {'status': 'success', 'data': user}, 201
            return {'status': 'failed', 'message': 'Password is too short. At least 8 characters required'}, 400
        return {'status': 'failed', 'message': 'Password and confirm password do not match, try again'}, 400

    def abort_if_email_is_already_used(self, email):
        user = [user for user in users if user['email'] == email]
        if len(user) != 0:
            abort(400, message='The email {} is already taken'.format(email))


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
        args = self.reqparse.parse_args()
        for user in users:
            if user['email'] == args['email'] and check_password_hash(user['password'], args['password']):
                return {'status': 'success', 'data': 'Login successful'}, 200
            return {'status': 'failed', 'data': 'Invalid email/password combination'}, 400


class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, location='json'
        )
        self.reqparse.add_argument(
            'lastname', type=str, location='json'
        )
        self.reqparse.add_argument(
            'email', type=str, location='json'
        )
        self.reqparse.add_argument(
            'car_registration', location='json'
        )
        self.reqparse.add_argument(
            'password', type=str, location='json'
        )

        super(UserResource, self).__init__()

    # GET method for a user
    def get(self, user_id):
        user = self.abort_if_user_doesnt_exist(user_id)
        return {'user': user[0]}

    # PUT method for editing a user
    def put(self, user_id):
        user = self.abort_if_user_doesnt_exist(user_id)
        user = user[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                user[k] = v
        return {'status': 'success', 'data': user}, 200

    # DELETE method for deleting a user
    def delete(self, user_id):
        user = self.abort_if_user_doesnt_exist(user_id)
        users.remove(user[0])
        return {'status': 'success', 'data': 'User successfully deleted'}, 200

    def abort_if_user_doesnt_exist(self, user_id):
        user = [user for user in users if user['id'] == int(user_id)]
        if len(user) == 0:
            abort(404, message='The user {} does not exist'.format(user_id))
        return user


users_v1_bp = Blueprint('resourcesV1.users', __name__)
api = Api(users_v1_bp)
api.add_resource(
    UserListResource, 
    '/api/v1/auth/signup',
    '/api/v1/auth/signup/'
    )
api.add_resource(
    LoginResource, 
    '/api/v1/auth/login',
    '/api/v1/auth/login/'
    )
api.add_resource(
    UserResource,
    '/api/v1/users/<user_id>',
    '/api/v1/users/<user_id>/'
    )
