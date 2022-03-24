"""
Package:        product_availability
Url Prefix:     /products/:product_id/availability
Description:    Handles all the product_availability routing.
"""


import flask
from http import HTTPStatus
from ..common import security
from ..models import ProductAvailability

from api_wmiys.services import products as product_services
from api_wmiys.services import product_availability as product_availability_services
from api_wmiys.common import responses


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


        availability.loadData() # load the current values into the object properties

        # set the objects properties to the fields in the request body
        if not availability.setPropertyValuesFromDict(flask.request.form.to_dict()):
            return ('Invalid request body field.', HTTPStatus.BAD_REQUEST.value)
    
        dbResult = availability.update()    # update the database
        return flask.jsonify(availability.get())
    
    elif flask.request.method == 'DELETE':
        row_count = availability.delete()

        if row_count != 1:
            pass    # error something went wrong
        
        return ('', HTTPStatus.NO_CONTENT.value)


