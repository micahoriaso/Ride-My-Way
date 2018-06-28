import os

from flaskr import create_app

import config




# if os.environ['FLASK_ENV'] == 'production':
#     configuration = config.ProductionConfig()
# else:
#     configuration = config.DevelopmentConfig()

app = create_app()
