import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB


class Car:
    def __init__(self):
        self.connection = connectDB()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    # method returns all cars
    def browse(self):
        try:
            self.cursor.execute('SELECT * FROM car;')
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        car_list = self.cursor.fetchall()
        if len(car_list) == 0:
            return {'status': 'success', 'message': 'There are no cars here'}, 202
        else:
            return {'status': 'success', 'message': 'Fetch successful', 'data': car_list}, 200

    # method returns the details of a car
    def read(self, car_registration):
        try:
            self.cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([car_registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(404, message='The car with licence plate  {} does not exist'.format(
                car_registration))
        return results

    # method for updating a car
    def edit(self, car_registration, model, capacity):
        try:
            self.cursor.execute(
                """
                UPDATE car SET 
                    model = %s,
                    capacity = %s
                WHERE id = %s;
                """,
                (
                    model,
                    capacity,
                    car_registration
                )
            )
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': 'Car successfully updated'}, 200

    # method for creating a new car
    def add(self, registration, model, capacity):
        try:
            self.cursor.execute(
                """INSERT INTO car (id, model, capacity) 
                VALUES (%s, %s, %s);""",
                (registration, model, capacity))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'message': 'Car created successfully'}, 201

    # method for deleting a car
    def delete(self, car_registration):
        try:
            self.cursor.execute('DELETE FROM car WHERE id = %s ;',
                                ([car_registration]))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        return {'status': 'success', 'data': 'Car successfully deleted'}, 200

    def abort_if_car_registration_is_already_used(self, registration):
        try:
            self.cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is not None:
            abort(400, message='The licence plate {} is already used'.format(
                registration))
        return results

    def abort_if_car_doesnt_exist(self, registration):
        try:
            self.cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = self.cursor.fetchone()
        if results is None:
            abort(404, message='The car with licence plate {} does not exist'.format(
                registration))
        return results
