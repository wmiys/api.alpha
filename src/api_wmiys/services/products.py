"""
**********************************************************************************************

Application logic for products.

**********************************************************************************************
"""


import flask
from api_wmiys.common import user_image
from ..models import Product
from ..common import responses

from api_wmiys.repository import products as proudcts_repo


#------------------------------------------------------
# Fetch all of a user's products
#------------------------------------------------------
def getAll():
    records = proudcts_repo.selectAll(flask.g.client_id)
    products = records.data

    # prepend the absolute image file path to each image field, if one exists
    for product in products:
        if product['image']:
            prefix = user_image.getCoverUrl()
            product['image'] = prefix + product['image']

    return products


#------------------------------------------------------
# Create a new product
#------------------------------------------------------
def post() -> flask.Response:
    new_product = Product(user_id=flask.g.client_id)

    # set the object properties from the fields in the request body
    if not new_product.setPropertyValuesFromDict(flask.request.form.to_dict()):
        return responses.badRequest('Request contained an invalid body field.')

    # save the image file to the server
    _updateImage(new_product)
    
    # save the product's info into the database
    new_product.insert()

    return responses.created(new_product.get())


#------------------------------------------------------
# Retrieve a single product
#------------------------------------------------------
def get(product_id) -> flask.Response:
    return responses.get(
        output = _loadProductBase(product_id).get()
    )

#------------------------------------------------------
# Update an existing product
#------------------------------------------------------
def put(product_id) -> flask.Response:
    product = _loadProductBase(product_id)

    # update the product's properties from the request dictionary
    if not product.setPropertyValuesFromDict(flask.request.form.to_dict()):
        return responses.badRequest('Invalid request body field.')

    _updateImage(product)

    if product.update() == -1:
        return responses.badRequest('Did not update product')
    else:
        return responses.updated()

#------------------------------------------------------
# Base method for generating a product object
#------------------------------------------------------
def _loadProductBase(product_id):
    # load the product data
    product = Product(id=product_id)
    product.loadData()  # load the product data from the database

    if product.user_id != flask.g.client_id:
        flask.abort(403)

    return product


#------------------------------------------------------
# Update the product's image property if one was included
#
# Returns a bool:
#   true: image was updated
#   false: image was NOT updated (included)
#------------------------------------------------------
def _updateImage(product: Product) -> bool:
    # set the image if one was uploaded
    product_image = flask.request.files.get('image')

    if not product_image:
        return False

    cover_directory = user_image.getCoverDirectory()
    product.setImagePropertyFromImageFile(product_image, cover_directory)

    return True

