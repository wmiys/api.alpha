"""
Package:        product_availability
Url Prefix:     /products/:product_id/availability
Description:    Handles all the product_availability routing.
"""

import flask
from api_wmiys.common import security
from api_wmiys.services import product_availability as product_availability_services

bp_product_availability = flask.Blueprint('productAvailabilityRoute', __name__)


#----------------------------------------------------------
# Retrieve all the product availabilities of a single product
# Or, create a new one
#----------------------------------------------------------
@bp_product_availability.route('', methods=['GET', 'POST'])
@security.login_required
@security.verify_product_owner
def productAvailabilities(product_id):

    if flask.request.method == 'POST':  # Create a new product availability
        return product_availability_services.responses_POST(product_id)
    else:                               # Retrieve all the product availabilities of a single product
        return product_availability_services.responses_GET_ALL(product_id)

#------------------------------------------------------
# GET single record
# PUT single record
# DELETE single record
#------------------------------------------------------
@bp_product_availability.route('<uuid:product_availability_id>', methods=['GET', 'PUT', 'DELETE'])
@security.login_required
@security.verify_product_owner
def productAvailability(product_id, product_availability_id):    
    
    if flask.request.method == 'PUT':
        return product_availability_services.responses_PUT(product_id, product_availability_id)
    elif flask.request.method == 'DELETE':
        return product_availability_services.responses_DELETE(product_availability_id)
    else:
        return product_availability_services.responses_GET(product_availability_id)
    


