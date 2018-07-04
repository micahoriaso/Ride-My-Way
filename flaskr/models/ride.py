import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB


class Ride:
    def __init__(self, date, time, pickup, dropoff, capacity, driver_id, price, status):
        self.date = date
        self.time = time
        self.pickup = pickup
        self.dropoff = dropoff
        self.capacity = capacity
        self.seats_available = capacity
        self.driver_id = driver_id
        self.price = price
        self.status = status


    # method returns all rides
    @staticmethod
    def browse():
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride;')
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_list = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(ride_list) == 0:
            return {'status': 'success', 'message': 'There are no rides offers yet'}, 202
        else:
            return {'status': 'success', 'message': 'Fetch successful', 'data': ride_list}, 200

    # method returns the details of a ride
    @staticmethod
    def read(ride_id):
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
            abort(
                404, message='The ride request with id {} does not exist'.format(ride_id)
                )
        return results

    # method for updating a ride
    @staticmethod
    def edit(date, time, pickup, dropoff, capacity, driver_id, price, status, ride_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        Ride.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            cursor.execute(
                """UPDATE ride SET 
                    date = %s,
                    time = %s,
                    pickup = %s,
                    dropoff = %s,
                    capacity = %s,
                    driver_id = %s,
                    price = %s,
                    status = %s
                 WHERE id = %s;""",
                (
                    date,
                    time,
                    pickup,
                    dropoff,
                    capacity,
                    driver_id,
                    price,
                    status,
                    ride_id
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride offer successfully updated'}, 200

    # method for creating a new ride request
    def add(self):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                """INSERT INTO ride (
                    date,
                    time,
                    pickup, 
                    dropoff,
                    capacity,
                    seats_available,
                    driver_id,
                    price,
                    status
                    ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (
                    self.date,
                    self.time,
                    self.pickup,
                    self.dropoff,
                    self.capacity,
                    self.seats_available,
                    self.driver_id,
                    self.price,
                    self.status
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'Ride created successfully'}, 201

    # method for deleting a ride
    @staticmethod
    def delete(ride_id):
        Ride.abort_if_ride_offer_doesnt_exist(ride_id)
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM ride WHERE id = %s ;',
                                ([ride_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        Ride.delete_this_rides_requests(ride_id)
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    #method for deleting a ride's requests
    @staticmethod
    def delete_this_rides_requests(ride_id):
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride requests successfully deleted'}, 200

    @staticmethod
    def abort_if_ride_offer_doesnt_exist(ride_id):
        return Ride.read(ride_id)

    @staticmethod
    def get_ride_car(ride_id):
        pass

    @staticmethod
    def get_ride_driver(ride_id):
            pass

    
