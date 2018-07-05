import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB


class Car:
    """A representation of a car.

    :param registration: A string, the car's licence plate.
    :param model: An int, the car's model.
    :param capacity: An int, the car's passenger capacity.
    """
    def __init__(self, registration, model, capacity):
        self.registration = registration
        self.model = model
        self.capacity = capacity

    @staticmethod
    def browse():
        """A method to get all cars.

        :return: A list of dictionaries with all rides
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car;')
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        car_list = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(car_list) == 0:
            return {'status': 'success', 'message': 'There are no cars here'}, 202
        else:
            data = []
            for car in car_list:
                item = {
                'registration':car['id'],
                'model':car['model'],
                'capacity':car['capacity']
                }
                data.append(item)
            return {'status': 'success', 'message': 'Fetch successful', 'data': data}, 200

    @staticmethod
    def read(car_registration):
        """
        A method to get the details of a car.
        :param car_registration: string, The car's licence plate
        :return: car details
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([car_registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The car with licence plate  {} does not exist'.format(
                car_registration))
        car = {
            'registration': results['id'],
            'model': results['model'],
            'capacity': results['capacity'],
        }
        return car

    @staticmethod
    def edit(car_registration, model, capacity):
        """
        A method to edit the details of a car.
        :param registration: A string, the car's licence plate.
        :param model: An int, the car's model.
        :param capacity: An int, the car's passenger capacity.
        :return: Http Response
        """
        Car.abort_if_car_doesnt_exist(car_registration)
        if Car.capacity_greater_than_zero(capacity):
            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute(
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
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            return {'status': 'success', 'data': 'Car successfully updated'}, 200
        return {'status': 'failed', 'message': 'Car capacity cannot be below one'}, 202

    def add(self):
        """
        A method to create a car.
        :return: Http Response
        """
        Car.abort_if_car_registration_is_already_used(self.registration)
        if Car.capacity_greater_than_zero(self.capacity):
            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute(
                    """INSERT INTO car (id, model, capacity) 
                    VALUES (%s, %s, %s);""",
                    (self.registration, self.model, self.capacity))
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            return {'status': 'success', 'message': 'Car created successfully'}, 201
        return {'status': 'failed', 'message': 'Car capacity cannot be below one'}, 202

    @staticmethod
    def delete(car_registration):
        """
        A method to delete a car.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        Car.abort_if_car_doesnt_exist(car_registration)
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM car WHERE id = %s ;',
                                ([car_registration]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Car successfully deleted'}, 200
    
    @staticmethod
    def abort_if_car_registration_is_already_used(registration):
        """
        A method to check if a car's liceence plate is unique.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            abort(400, message='The licence plate {} is already used'.format(
                registration))
        return results

    @staticmethod
    def abort_if_car_doesnt_exist(registration):
        """
        A method to check if a car exists in the database.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        return Car.read(registration)

    @staticmethod
    def capacity_greater_than_zero(capacity):
        """
        A method to check if a car's capacity is greater than zero.
        :param capacity: An int, the car's passenger capacity.
        :return: Http Response
        """
        if capacity > 0:
            return True
        return False        
