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


#----------------------------------------------------------
# Sets up and initializes the flask application
#----------------------------------------------------------
def initApp(flaskApp: Flask):    
    flaskApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0        # remove cacheing
    flaskApp.config['JSON_SORT_KEYS'] = False               # don't sort the json keys
    flaskApp.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # print the json pretty
    flaskApp.json_encoder = CustomJSONEncoder               # setup the custom encoder for dates
    CORS(flaskApp)                                          # setup the CORS policy


#----------------------------------------------------------
# Register all of the Flask blueprints
#----------------------------------------------------------
def registerBlueprints(flaskApp: Flask):
    flaskApp.register_blueprint(routes.product_categories.bp_product_categories, url_prefix='/product-categories')
    flaskApp.register_blueprint(routes.users.bp_users, url_prefix='/users')
    flaskApp.register_blueprint(routes.products.bp_products, url_prefix='/products')
    flaskApp.register_blueprint(routes.product_availability.bp_product_availability, url_prefix='/products/<int:product_id>/availability')
    flaskApp.register_blueprint(routes.product_images.bp_product_images, url_prefix='/products/<int:product_id>/images')
    flaskApp.register_blueprint(routes.login.bp_login, url_prefix='/login')
    flaskApp.register_blueprint(routes.search.bp_search, url_prefix='/search')
    flaskApp.register_blueprint(routes.search_products.bp_search_products, url_prefix='/search/products')
    flaskApp.register_blueprint(routes.listings.bp_listings, url_prefix='/listings/<int:product_id>')
    flaskApp.register_blueprint(routes.locations.bp_locations, url_prefix='/locations')
    flaskApp.register_blueprint(routes.requests.bp_requests, url_prefix='/requests')
    flaskApp.register_blueprint(routes.payments.bp_payments, url_prefix='/payments')

app = Flask(__name__)

initApp(app)
registerBlueprints(app)
