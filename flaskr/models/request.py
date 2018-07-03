import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB


class RideRequest:
    def __init__(self):
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    # method returns all ride requests
    def browse(self, ride_id):
        try:
            self.cursor.execute('SELECT id, ride_id, requestor_id, request_status FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_offer_request = self.cursor.fetchall()
        if len(ride_offer_request) == 0:
            return {'status': 'success', 'message': 'No requests available for this ride yet'}, 202
        else:
            return {'status': 'success', 'message': 'Fetch successful', 'data': ride_offer_request}

    # method returns the details of a ride request
    def read(self, request_id):
        try:
            self.cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(
                404, message='The ride request with id {} does not exist'.format(request_id)
            )
        return results

    # method for updating a ride request
    def edit(self, request_id, request_status):
        try:
            self.cursor.execute('UPDATE ride_request SET request_status = %s WHERE id = %s;',
                                (request_status, request_id))

            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500

        return {'status': 'success', 'data': 'Ride request successfully updated'}, 200

    # method for creating a new ride request
    def add(self, ride_id, requestor_id, request_status):
        try:
            self.cursor.execute(
                """INSERT INTO ride_request (ride_id, requestor_id, request_status) 
                VALUES (%s, %s, %s);""",
                (ride_id, requestor_id, request_status))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'message': 'Ride requested successfully'}, 201

    # method for deleting a ride request
    def delete(self, request_id):
        try:
            self.cursor.execute('DELETE FROM ride_request WHERE id = %s ;',
                                ([request_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500

        return {'status': 'success', 'message': 'Ride request successfully deleted'}, 200

    def abort_if_ride_offer_doesnt_exist(self, ride_id):
        try:
            self.cursor.execute('SELECT * FROM ride WHERE id = %s ;',
                                ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(404, message='The ride with id {} does not exist'.format(ride_id))

    def abort_if_ride_request_doesnt_exist(self, request_id):
        try:
            self.cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(
                404, message='The ride request with id {} does not exist'.format(request_id))
        return results
