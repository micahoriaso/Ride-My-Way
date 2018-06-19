from flask import Flask

def create_app(test_config=None):
    # Create an instance of the flask application
    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    
    # Apply blueprints to the app
    from flaskr import rides
    app.register_blueprint(rides.bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app

