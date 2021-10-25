"""
Package:        products
Url Prefix:     /products
Description:    Handles all the products routing.
"""

import flask
from http import HTTPStatus
from ..common import security
from ..models import Product
from ..models.product import LOCAL_SERVER_COVER_PHOTO_DIRECTORY

products = flask.Blueprint('products', __name__)

#------------------------------------------------------
# Fetch all of a user's products
#------------------------------------------------------
@products.route('', methods=['GET'])
@security.login_required
def userProductsGet():
    userProducts = Product.getAll(security.requestGlobals.client_id)
    return flask.jsonify(userProducts)


#------------------------------------------------------
# Create a new product
#------------------------------------------------------
@products.route('', methods=['POST'])
@security.login_required
def userProductsPost():
    newProduct = Product(user_id=security.requestGlobals.client_id)

    # set the object properties from the fields in the request body
    # if the request body contains an invalid field, abort
    if not newProduct.setPropertyValuesFromDict(flask.request.form.to_dict()):
        return ('Request contained an invalid body field.', HTTPStatus.BAD_REQUEST.value)

    # set the image if one was uploaded
    if flask.request.files.get('image'):
        newProduct.setImagePropertyFromImageFile(flask.request.files.get('image'), f'{flask.current_app.static_folder}{LOCAL_SERVER_COVER_PHOTO_DIRECTORY}')

    newProduct.insert()

    return flask.jsonify(newProduct.get())


#------------------------------------------------------
# Retrieve or update an existing product
#------------------------------------------------------
@products.route('<int:product_id>', methods=['GET', 'PUT'])
@security.login_required
def productRequest(product_id):
    # load the product data
    product = Product(id=product_id)
    product.loadData()  # load the product data from the database

    if product.user_id != security.requestGlobals.client_id:
        return ('', HTTPStatus.FORBIDDEN.value)

    if flask.request.method != 'PUT':
        return flask.jsonify(product.get())
    else:
        # update the product's properties from the request dictionary
        if not product.setPropertyValuesFromDict(flask.request.form.to_dict()):
            return ('Invalid request body field.', HTTPStatus.BAD_REQUEST.value)

        # set the image if one was uploaded
        if flask.request.files.get('image'):
            product.setImagePropertyFromImageFile(flask.request.files.get('image'), f'{flask.current_app.static_folder}product-images/covers')

        records_updated = product.update()

        if records_updated == -1:
            return ('Did not update product', HTTPStatus.BAD_REQUEST.value)
        else:
            return ('', HTTPStatus.OK.value)
            
        
