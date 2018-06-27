import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connectDB():
    connection_string = 'dbname=ride_my_way user=oriaso password=root100 host=localhost'
    try:
        return psycopg2.connect(connection_string)
    except:
        print('Can\'t connect to database')

def create_db_tables():
    queries = [
        """
        CREATE TABLE ride (
            id SERIAL PRIMARY KEY NOT NULL, 
            pickup CHAR(140) NOT NULL, 
            dropoff CHAR(140) NOT NULL, 
            capacity INT NOT NULL, 
            seats_available INT NOT NULL, 
            driver_id INT NOT NULL, 
            registration CHAR(140) NOT NULL, 
            price REAL NOT NULL, 
            status CHAR(140) NOT NULL
            );
        """,
        """
        CREATE TABLE ride_request (
            id SERIAL PRIMARY KEY NOT NULL, 
            ride_id INT NOT NULL, 
            requestor_id INT NOT NULL, 
            request_status CHAR(140) NOT NULL
            );
        """,
        """
        CREATE TABLE app_user (
            id SERIAL PRIMARY KEY NOT NULL, 
            firstname CHAR(140) NOT NULL, 
            lastname CHAR(140) NOT NULL, 
            fullname CHAR(140) NOT NULL, 
            email CHAR(140) NOT NULL, 
            password CHAR(140) NOT NULL, 
            car_registration CHAR(140)
            );
        """,
        """
        CREATE TABLE car (
            id CHAR(140) PRIMARY KEY NOT NULL, 
            model CHAR(140) NOT NULL, 
            capacity INT NOT NULL);
        """
    ]
    run_query_commands(queries)

def run_query_commands(queries):
    connection = None
    try:
       connection = connectDB()
       cursor = connection.cursor()
       for query in queries:
            cursor.execute(query)
       cursor.close()
       connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_db_tables()
