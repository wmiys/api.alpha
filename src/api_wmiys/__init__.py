"""
Available Routes:


Resource             | URI
---------------------|---------------------------------------------------------------------------
User                 | /users/:user_id
Products             | /products/:product_id
Product Availability | /products/:product_id/availability/:product_availability_id
Product Images       | /products/:product_id/images/:product_image_id
Listings             | /listings/:product_id
Product Categories   | /product-categories
Login                | /login
Locations            | /locations/:location_id
Search Locations     | /search/locations
Search Products      | /search/products
Requests             | /requests
Payments             | /payments

"""

from flask import Flask
from flask_cors import CORS
from .common import CustomJSONEncoder
from . import routes

def initApp(flaskApp):
    """Sets up and initializes the flask application

    Args:
        flaskApp (obj): the flask application
    """
    
    flaskApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0        # remove cacheing
    flaskApp.config['JSON_SORT_KEYS'] = False               # remove cacheing
    flaskApp.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # remove cacheing
    flaskApp.json_encoder = CustomJSONEncoder               # setup the custom encoder for dates
    CORS(flaskApp)                                          # setup the CORS policy


def registerBlueprints(flaskApp):
    """Register all of the Flask blueprints

    Args:
        flaskApp (obj): the flask application
    """
    flaskApp.register_blueprint(routes.product_categories.bp_product_categories, url_prefix='/product-categories')
    flaskApp.register_blueprint(routes.users.routeUser, url_prefix='/users')
    flaskApp.register_blueprint(routes.products.products, url_prefix='/products')
    flaskApp.register_blueprint(routes.product_availability.productAvailabilityRoute, url_prefix='/products/<int:product_id>/availability')
    flaskApp.register_blueprint(routes.product_images.bpProductImages, url_prefix='/products/<int:product_id>/images')
    flaskApp.register_blueprint(routes.login.login, url_prefix='/login')
    flaskApp.register_blueprint(routes.search.search, url_prefix='/search')
    flaskApp.register_blueprint(routes.search_products.searchProducts, url_prefix='/search/products')
    flaskApp.register_blueprint(routes.listings.productListings, url_prefix='/listings/<int:product_id>')
    flaskApp.register_blueprint(routes.locations.locationsBP, url_prefix='/locations')
    flaskApp.register_blueprint(routes.requests.bp_requests, url_prefix='/requests')
    flaskApp.register_blueprint(routes.payments.bp_payments, url_prefix='/payments')

app = Flask(__name__)

initApp(app)
registerBlueprints(app)
