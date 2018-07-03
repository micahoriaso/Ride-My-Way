import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB


class Ride:
    def __init__(self):
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    # method returns all rides
    def browse(self):
        try:
            self.cursor.execute('SELECT * FROM ride;')
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_list = self.cursor.fetchall()
        if len(ride_list) == 0:
            return {'status': 'success', 'message': 'There are no rides offers yet'}, 202
        else:
            return {'status': 'success', 'message': 'Fetch successful', 'data': ride_list}, 200

    # method returns the details of a ride
    def read(self, request_id):
        try:
            self.cursor.execute('SELECT * FROM ride WHERE id = %s ;',
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

    # method for updating a ride
    def edit(self, date, time, pickup, dropoff, capacity, available_seats, driver_id, registration, price, status, ride_id):
        try:
            self.cursor.execute(
                """UPDATE ride SET 
                    date = %s,
                    time = %s,
                    pickup = %s,
                    dropoff = %s,
                    capacity = %s,
                    seats_available = %s,
                    driver_id = %s,
                    registration = %s,
                    price = %s,
                    status = %s
                 WHERE id = %s;""",
                (
                    date,
                    time,
                    pickup,
                    dropoff,
                    capacity,
                    available_seats,
                    driver_id,
                    registration,
                    price,
                    status,
                    ride_id
                )
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': 'Ride offer successfully updated'}, 200

    # method for creating a new ride request
    def add(self, date, time, pickup, dropoff, capacity, available_seats, driver_id, registration, price, status):
        try:
            self.cursor.execute(
                """INSERT INTO ride (
                    date,
                    time,
                    pickup, 
                    dropoff,
                    capacity,
                    seats_available,
                    driver_id,
                    registration,
                    price,
                    status
                    ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (
                    date,
                    time,
                    pickup,
                    dropoff,
                    capacity,
                    available_seats,
                    driver_id,
                    registration,
                    price,
                    status
                )
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'message': error}, 500
        return {'status': 'success', 'message': 'Ride creation successful'}, 201

    # method for deleting a ride
    def delete(self, ride_id):
        try:
            self.cursor.execute('DELETE FROM ride WHERE id = %s ;',
                                ([ride_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        self.delete_this_rides_requests(ride_id)
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    def delete_this_rides_requests(self, ride_id):
        try:
            self.cursor.execute('DELETE FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': 'Ride requests successfully deleted'}, 200

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
        return results