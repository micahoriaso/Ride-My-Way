import psycopg2
import psycopg2.extras

def connectDB():
    connection_string = 'dbname=ride_my_way user=oriaso password=root100 host=localhost'
    try:
        return psycopg2.connect(connection_string)
    except:
        print('Can\'t connect to database')


def create_tables():
    command = """
        CREATE TABLE ride_requests (id SERIAL PRIMARY KEY NOT NULL, ride_id INT NOT NULL, requestor_id INT NOT NULL, request_status CHAR(140) NOT NULL);
    """
    connection = None
    try:
       connection = connectDB()
       cursor = connection.cursor()
       cursor.execute(command)
       cursor.close()
       connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
