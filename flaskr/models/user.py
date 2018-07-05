import datetime
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token

from flask_restful import abort

from flaskr.db import connectDB

from flaskr.models.car import Car

class User:
    def __init__(self, firstname, lastname, email, password, phone_number=None, car_registration=None):
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = '{} {}'.format(firstname, lastname)
        self.email = email
        self.phone_number = phone_number
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
        self.car_registration = car_registration

    # method returns the details of a user
    @staticmethod
    def read(user_id):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE id = %s ;',
                           ([user_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The user with id {} does not exist'.format(user_id))
        user = {
            'id': results['id'],
            'firstname': results['firstname'],
            'lastname': results['lastname'],
            'fullname': results['fullname'],
            'email': results['email'],
            'phone_number': results['phone_number'],
            'password': results['password'],
            'car_registration': results['car_registration']
        }
        return user

    # method for updating a user
    @staticmethod
    def edit(user_id, firstname, lastname, password, phone_number=None, car_registration=None):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_user_doesnt_exist(user_id)
        User.abort_if_car_doesnt_exist(car_registration)
        try:
            cursor.execute(
                """UPDATE app_user SET
                    firstname = %s,
                    lastname = %s,
                    fullname = %s,
                    phone_number = %s,
                    password = %s,
                    car_registration = %s
                WHERE id = %s;""",
                (
                    firstname,
                    lastname,
                    '{} {}'.format(
                        firstname, lastname
                    ),
                    phone_number,
                    generate_password_hash(
                        password,
                        method='sha256'
                    ),
                    car_registration,
                    int(user_id)
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'User updated successfully'}, 200

    # method for creating a new user
    def add(self):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_email_is_already_used(self.email)
        try:
            cursor.execute(
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
                    self.firstname,
                    self.lastname,
                    self.fullname,
                    self.email,
                    self.phone_number,
                    self.password,
                    self.car_registration
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 500
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=self.email, expires_delta=expires)
        cursor.close()
        connection.close()
        return {
            'status': 'success', 
            'message': 'Account creation successful',
            'access_token': access_token,
            }, 201

    @staticmethod
    def login(email, password):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            if results['email'] == email and check_password_hash(results['password'], password):
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(
                    identity=email, expires_delta=expires)
                return {
                    'status': 'success',
                    'message': 'Login successful',
                    'access_token': access_token,
                }, 200
            return {'status': 'failed', 'message': 'Wrong password, please try again'}, 202
        else:
            abort(404, message='The user with email {} does not exist'.format(
                email))

    # method for deleting a user
    @staticmethod
    def delete(user_id):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_user_doesnt_exist(user_id)
        try:
            cursor.execute('DELETE FROM app_user WHERE id = %s ;',
                                ([user_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 200
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'User successfully deleted'}, 200

    @staticmethod
    def abort_if_user_doesnt_exist(user_id):
        return User.read(user_id)

    @staticmethod
    def abort_if_email_is_already_used(email):
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            abort(400, message='The email {} is already taken'.format(email))
        return results

    @staticmethod
    def abort_if_car_doesnt_exist(registration):
        if registration is not None:
            connection = connectDB()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute('SELECT * FROM car WHERE id = %s ;',
                            ([registration]))
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            results = cursor.fetchone()
            cursor.close()
            connection.close()
            if results is None:
                abort(404, message='The car with licence plate {} cannot be found in our records'.format(
                    registration))
            return results

    @staticmethod
    def get_car(user_id):
        user = User.read(user_id)
        if user['car_registration'] is None:
            abort(404, message='You have no car yet, enter your car details first to proceed')
        return Car.read(user['car_registration'])
