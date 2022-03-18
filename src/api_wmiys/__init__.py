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
import wmiys_common
from .common import CustomJSONEncoder
from .common import user_image
from . import db
from . import routes


#----------------------------------------------------------
# Sets up and initializes the flask application
#----------------------------------------------------------
def initApp(flask_app: Flask):    
    flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0        # remove cacheing
    flask_app.config['JSON_SORT_KEYS'] = False               # don't sort the json keys
    flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  # print the json pretty
    flask_app.json_encoder = CustomJSONEncoder               # setup the custom encoder for dates
    CORS(flask_app)                                          # setup the CORS policy


#----------------------------------------------------------
# Sets up and initializes the flask application (NEW WAY)
#----------------------------------------------------------
def configureApp(flask_app: Flask):
    # set the flask configuration values for either production or development
    if flask_app.env == "production":
        flask_app.config.from_object(wmiys_common.config.Production)
    else:
        flask_app.config.from_object(wmiys_common.config.Dev)

    # setup the custom encoder for dates
    flask_app.json_encoder = CustomJSONEncoder

    # setup the CORS policy
    CORS(flask_app)

    configureAppOldWay(flask_app)
    

def configureAppOldWay(flask_app: Flask):
    # api url
    api_url = flask_app.config.get('URL_API')
    user_image.STATIC_URL_PREFIX = f'{api_url}/'

    # database connection host
    db.credentials.HOST = flask_app.config.get('DB_HOST')



#----------------------------------------------------------
# Register all of the Flask blueprints
#----------------------------------------------------------
def registerBlueprints(flask_app: Flask):
    flask_app.register_blueprint(routes.product_categories.bp_product_categories, url_prefix='/product-categories')
    flask_app.register_blueprint(routes.users.bp_users, url_prefix='/users')
    flask_app.register_blueprint(routes.products.bp_products, url_prefix='/products')
    flask_app.register_blueprint(routes.product_availability.bp_product_availability, url_prefix='/products/<int:product_id>/availability')
    flask_app.register_blueprint(routes.product_images.bp_product_images, url_prefix='/products/<int:product_id>/images')
    flask_app.register_blueprint(routes.login.bp_login, url_prefix='/login')
    flask_app.register_blueprint(routes.search.bp_search, url_prefix='/search')
    flask_app.register_blueprint(routes.search_products.bp_search_products, url_prefix='/search/products')
    flask_app.register_blueprint(routes.listings.bp_listings, url_prefix='/listings/<int:product_id>')
    flask_app.register_blueprint(routes.locations.bp_locations, url_prefix='/locations')
    flask_app.register_blueprint(routes.requests.bp_requests, url_prefix='/requests')
    flask_app.register_blueprint(routes.payments.bp_payments, url_prefix='/payments')
    flask_app.register_blueprint(routes.payout_accounts.bp_payout_accounts, url_prefix='/payout-accounts')
    flask_app.register_blueprint(routes.balance_transfers.bp_balance_transfers, url_prefix='/balance-transfers')
    flask_app.register_blueprint(routes.password_resets.bp_password_resets, url_prefix='/password-resets')

app = Flask(__name__)

# initApp(app)
configureApp(app)

registerBlueprints(app)
