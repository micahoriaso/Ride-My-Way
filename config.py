class BaseConfig:
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    connection_string = 'dbname=ride_my_way user=oriaso password=root100 host=localhost'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    connection_string = ''

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    connection_string = ''
