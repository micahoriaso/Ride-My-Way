import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB

class RideRequest:
    def __init__(self, ride_id, requestor_id, request_status):
        self.ride_id = ride_id
        self.requestor_id = requestor_id
        self.request_status = request_status

    # method returns all ride requests
    @staticmethod
    def browse(ride_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            cursor.execute('SELECT id, ride_id, requestor_id, request_status FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_offer_request = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(ride_offer_request) == 0:
            return {'status': 'success', 'message': 'No requests available for this ride yet'}, 404
        else:
            return {'status': 'success', 'message': 'Fetch successful', 'data': ride_offer_request}

    # method returns the details of a ride request
    @staticmethod
    def read(ride_id,request_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        RideRequest.abort_if_ride_request_doesnt_exist(request_id)
        try:
            cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()

        if results is None:
            abort(
                404, message='The ride request with id {} does not exist'.format(request_id)
            )
        return results

    # method for updating a ride request
    @staticmethod
    def edit(ride_id, request_id, request_status):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        RideRequest.abort_if_ride_request_doesnt_exist(request_id)
        try:
            cursor.execute('UPDATE ride_request SET request_status = %s WHERE id = %s;',
                                (request_status, request_id))

            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride request successfully updated'}, 200

    # method for creating a new ride request
    def add(self):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(self.ride_id)
        RideRequest.abort_if_requestor_doesnt_exist(self.requestor_id)
        try:
            cursor.execute(
                """INSERT INTO ride_request (ride_id, requestor_id, request_status) 
                VALUES (%s, %s, %s);""",
                (self.ride_id, self.requestor_id, self.request_status))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'Ride requested successfully'}, 201

    # method for deleting a ride request
    @staticmethod
    def delete(ride_id, request_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        RideRequest.abort_if_ride_request_doesnt_exist(request_id)
        try:
            cursor.execute('DELETE FROM ride_request WHERE id = %s ;',
                                ([request_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'Ride request successfully deleted'}, 200

    @staticmethod
    def abort_if_ride_offer_doesnt_exist(ride_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s ;',
                                ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The ride with id {} does not exist'.format(ride_id))
        return results

    @staticmethod
    def abort_if_ride_request_doesnt_exist(request_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The ride request with id {} does not exist'.format(request_id))
        return results

    @staticmethod
    def abort_if_requestor_doesnt_exist(requestor_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE id = %s ;',
                                ([requestor_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()

        if results is None:
            abort(404, message='The user with id {} does not exist'.format(requestor_id))
        return results
