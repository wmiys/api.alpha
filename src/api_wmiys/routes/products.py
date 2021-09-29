"""
Package:        products
Url Prefix:     /users/<int:user_id>/products
Description:    Handles all the products routing.
"""

import flask
from flask import Blueprint, jsonify, request
from ..db import DB
from ..common import security
from ..models import Product
from ..models.product import LOCAL_SERVER_COVER_PHOTO_DIRECTORY

products = Blueprint('products', __name__)

#------------------------------------------------------
# Fetch all of a user's products
#------------------------------------------------------
@products.route('', methods=['GET'])
@security.login_required
def userProductsGet(user_id):
    # make sure the user is authorized
    if security.requestGlobals.client_id != user_id:
        flask.abort(403)

    # userProducts = DB.getUserProducts(user_id)
    userProducts = Product.getAll(user_id)

    return jsonify(userProducts)


#------------------------------------------------------
# Create a new product
#------------------------------------------------------
@products.route('', methods=['POST'])
@security.login_required
def userProductsPost(user_id):
    # make sure the user is authorized
    if security.requestGlobals.client_id != user_id:
        flask.abort(403)

    newProduct = Product()

    # set the object properties from the fields in the request body
    # if the request body contains an invalid field, abort
    if not newProduct.setPropertyValuesFromDict(request.form.to_dict()):
        flask.abort(400)

    newProduct.user_id = user_id    # user_id is in the URI

    # set the image if one was uploaded
    if request.files.get('image'):
        newProduct.setImagePropertyFromImageFile(request.files.get('image'), LOCAL_SERVER_COVER_PHOTO_DIRECTORY)

    newProduct.insert()

    return jsonify(newProduct.get())


#------------------------------------------------------
# Retrieve or update an existing product
#------------------------------------------------------
@products.route('<int:product_id>', methods=['GET', 'PUT'])
@security.login_required
def productRequest(user_id, product_id):
    # load the product data
    product = Product(id=product_id)
    product.loadData()  # load the product data from the database

    if request.method == 'PUT':
        # update the product's properties from the request dictionary
        if not product.setPropertyValuesFromDict(request.form.to_dict()):
            # the request body contained a field that does not belong in the product class
            flask.abort(400)

        # set the image if one was uploaded
        if request.files.get('image'):
            product.setImagePropertyFromImageFile(request.files.get('image'), LOCAL_SERVER_COVER_PHOTO_DIRECTORY)


        records_updated = product.update()

        if records_updated == -1:
            return ('Did not update product', 400)
        else:
            return ('', 200)
            
    else:
        return jsonify(product.get())
