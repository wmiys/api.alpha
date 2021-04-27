"""
Package:        product_availability
Url Prefix:     /users/:user_id/products/:product_id/availability
Description:    Handles all the product_availability routing.
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from api_wmiys.product_availability.Product_Availability import ProductAvailability

productAvailabilityRoute = Blueprint('productAvailabilityRoute', __name__)


@productAvailabilityRoute.route('', methods=['GET'])
@Security.login_required
def productAvailabilities(user_id: int, product_id: int):
    """Retrieve all the product availabilities of a single product

    Args:
        user_id (int): the user's id
        product_id (int): the product id

    Returns:
        list: list of all the product availability records for a single product
    """

    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    # get the availabilities
    availabilities = ProductAvailability.getProductAvailabilities(product_id)
    return jsonify(availabilities)


@productAvailabilityRoute.route('', methods=['POST'])
@Security.login_required
def productAvailabilityPost(user_id: int, product_id: int):
    """Create a new product availability

    Args:
        user_id (int): user id
        product_id (int): product id
    """
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

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
@Security.login_required
def productAvailability(user_id: int, product_id: int, product_availability_id: int):
    """Retrieve all the product availabilities of a single product

    Args:
        user_id (int): user id
        product_id (int): product id
        product_availability_id (int): the product_availability id
    """
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

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
        result = availability.delete()

        if result.rowcount != 1:
            pass    # error something went wrong
        
        return ('', 204)