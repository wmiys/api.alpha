"""
Package:        product_availability
Url Prefix:     /products/:product_id/availability
Description:    Handles all the product_availability routing.
"""

import flask
from http import HTTPStatus
from ..common import security
from ..models import ProductAvailability, product

bp_product_availability = flask.Blueprint('productAvailabilityRoute', __name__)


#----------------------------------------------------------
# Retrieve all the product availabilities of a single product
#----------------------------------------------------------
@bp_product_availability.route('', methods=['GET'])
@security.login_required
def productAvailabilities(product_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, flask.g.client_id):
        return ('', HTTPStatus.FORBIDDEN.value)

    # get the availabilities
    availabilities = ProductAvailability.getProductAvailabilities(product_id)
    return flask.jsonify(availabilities)


#----------------------------------------------------------
# Create a new product availability
#----------------------------------------------------------
@bp_product_availability.route('', methods=['POST'])
@security.login_required
def productAvailabilityPost(product_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, flask.g.client_id):
        return ('', HTTPStatus.FORBIDDEN.value)

    # get the availabilities
    availability = ProductAvailability(product_id=product_id)
    
    # set the objects properties to the fields in the request body
    if not availability.setPropertyValuesFromDict(flask.request.form.to_dict()):
        return ('Invalid request body field.', HTTPStatus.BAD_REQUEST.value)
    
    availability.insert()

    return flask.jsonify(availability.get())


#------------------------------------------------------
# Retrieve all the product availabilities of a single product
#------------------------------------------------------
@bp_product_availability.route('<int:product_availability_id>', methods=['GET', 'PUT', 'DELETE'])
@security.login_required
def productAvailability(product_id: int, product_availability_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, flask.g.client_id):
        return ('', HTTPStatus.FORBIDDEN.value)

    availability = ProductAvailability(id=product_availability_id)
    
    if flask.request.method == 'GET':
        return flask.jsonify(availability.get())
    
    elif flask.request.method == 'PUT':
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