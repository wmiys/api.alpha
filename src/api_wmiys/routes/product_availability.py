"""
Package:        product_availability
Url Prefix:     /products/:product_id/availability
Description:    Handles all the product_availability routing.
"""

import flask
from http import HTTPStatus
from api_wmiys.common import security
from api_wmiys.models import ProductAvailability
from api_wmiys.services import product_availability as product_availability_services


bp_product_availability = flask.Blueprint('productAvailabilityRoute', __name__)



#----------------------------------------------------------
# Retrieve all the product availabilities of a single product
#----------------------------------------------------------
@bp_product_availability.get('')
@security.login_required
@security.verify_product_owner
def productAvailabilities(product_id):
    return product_availability_services.responses_GET_ALL(product_id)


#----------------------------------------------------------
# Create a new product availability
#----------------------------------------------------------
@bp_product_availability.post('')
@security.login_required
@security.verify_product_owner
def productAvailabilityPost(product_id):
    return product_availability_services.responses_POST(product_id)


#------------------------------------------------------
# Retrieve all the product availabilities of a single product
#------------------------------------------------------
@bp_product_availability.route('<uuid:product_availability_id>', methods=['GET', 'PUT', 'DELETE'])
@security.login_required
@security.verify_product_owner
def productAvailability(product_id, product_availability_id):

    availability = ProductAvailability(id=product_availability_id)
    
    if flask.request.method == 'GET':
        return flask.jsonify(availability.get())
    
    elif flask.request.method == 'PUT':
        return product_availability_services.responses_PUT(product_id, product_availability_id)
    
    elif flask.request.method == 'DELETE':
        row_count = availability.delete()

        if row_count != 1:
            pass    # error something went wrong
        
        return ('', HTTPStatus.NO_CONTENT.value)


