from flask import Flask
from flask_cors import CORS
from api_wmiys.common.CustomJSONEncoder import CustomJSONEncoder
from api_wmiys.product_categories.controllers import product_categories
from api_wmiys.products.controllers import products
from api_wmiys.users.controllers import routeUser
from api_wmiys.login.controllers import login
from api_wmiys.search.controllers import search
from api_wmiys.product_availability.controllers import productAvailabilityRoute
from api_wmiys.search_products.controllers import searchProducts


def initApp(flaskApp):
    """Sets up and initializes the flask application

    Args:
        flaskApp (obj): the flask application
    """
    
    flaskApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0    # remove cacheing
    flaskApp.json_encoder = CustomJSONEncoder           # setup the custom encoder for dates
    CORS(flaskApp)                                      # setup the CORS policy


def registerBlueprints(flaskApp):
    """Register all of the Flask blueprints

    Args:
        flaskApp (obj): the flask application
    """
    flaskApp.register_blueprint(product_categories, url_prefix='/product-categories')
    flaskApp.register_blueprint(routeUser, url_prefix='/users')
    flaskApp.register_blueprint(products, url_prefix='/users/<int:user_id>/products')
    flaskApp.register_blueprint(productAvailabilityRoute, url_prefix='/users/<int:user_id>/products/<int:product_id>/availability')
    flaskApp.register_blueprint(login, url_prefix='/login')
    flaskApp.register_blueprint(search, url_prefix='/search')
    flaskApp.register_blueprint(searchProducts, url_prefix='/search/products')


app = Flask(__name__)

initApp(app)
registerBlueprints(app)
