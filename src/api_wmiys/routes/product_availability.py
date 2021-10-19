"""
Package:        product_availability
Url Prefix:     /products/:product_id/availability
Description:    Handles all the product_availability routing.
"""

import flask
from flask import Blueprint, jsonify, request
from ..common import security
from ..models import ProductAvailability, product

productAvailabilityRoute = Blueprint('productAvailabilityRoute', __name__)


#----------------------------------------------------------
# Retrieve all the product availabilities of a single product
#----------------------------------------------------------
@productAvailabilityRoute.route('', methods=['GET'])
@security.login_required
def productAvailabilities(product_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, security.requestGlobals.client_id):
        return ('', 403)

    # get the availabilities
    availabilities = ProductAvailability.getProductAvailabilities(product_id)
    return jsonify(availabilities)


#----------------------------------------------------------
# Create a new product availability
#----------------------------------------------------------
@productAvailabilityRoute.route('', methods=['POST'])
@security.login_required
def productAvailabilityPost(product_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, security.requestGlobals.client_id):
        return ('', 403)

    # get the availabilities
    availability = ProductAvailability(product_id=product_id)
    
    # set the objects properties to the fields in the request body
    if not availability.setPropertyValuesFromDict(request.form.to_dict()):
        flask.abort(400)    # the request body contained a field that does not belong in the product class
    
    availability.insert()

    return jsonify(availability.get())


#------------------------------------------------------
# Retrieve all the product availabilities of a single product
#------------------------------------------------------
@productAvailabilityRoute.route('<int:product_availability_id>', methods=['GET', 'PUT', 'DELETE'])
@security.login_required
def productAvailability(product_id: int, product_availability_id: int):
    # verify that the user owns the product 
    if not product.doesUserOwnProduct(product_id, security.requestGlobals.client_id):
        return ('', 403)

    availability = ProductAvailability(id=product_availability_id)
    
    if request.method == 'GET':
        return jsonify(availability.get())
    
    elif request.method == 'PUT':
        availability.loadData() # load the current values into the object properties

        # set the objects properties to the fields in the request body
        if not availability.setPropertyValuesFromDict(request.form.to_dict()):
            flask.abort(400)    # the request body contained a field that does not belong in the product class
    
        dbResult = availability.update()    # update the database
        return jsonify(availability.get())
    
    elif request.method == 'DELETE':
        row_count = availability.delete()

        if row_count != 1:
            pass    # error something went wrong
        
        return ('', 204)