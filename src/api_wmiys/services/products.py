"""
**********************************************************************************************

Application logic for products.

**********************************************************************************************
"""


import os
import flask
from wmiys_common import utilities
from api_wmiys.common import user_image
from ..models import Product
from ..common import responses
from .. import common  

from api_wmiys.repository import products as proudcts_repo

from api_wmiys.domain import models
from api_wmiys.common import serializers


#------------------------------------------------------
# Responsd to a GET all request
#------------------------------------------------------
def responseGetAll() -> flask.Response:
    products = getAllProducts()
    return responses.get(products)


#------------------------------------------------------
# Retrieve all the user's products
#------------------------------------------------------
def getAllProducts():
    products = proudcts_repo.selectAll(flask.g.client_id).data

    for product in products:
        setImageUrlPrefix(product)

    return products

#------------------------------------------------------
# Prepend the absolute image file path to each image field, if one exists
#------------------------------------------------------
def setImageUrlPrefix(product: dict):
    if product['image']:
        prefix = user_image.getCoverUrl()
        product['image'] = prefix + product['image']


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
# Create a new product
#------------------------------------------------------
def responsePost() -> flask.Response:
    # fetch the incoming request data dict
    # all the data for the new product should be in here
    in_data = flask.request.form.to_dict()

    # serialize the incoming request data form into a product domain model
    serialize_result = serializers.ProductSerializer(in_data).serialize()

    if not serialize_result.successful:
        return responses.badRequest('Request contained an invalid body field.')

    # now, prepare the product model to insert into the database
    new_product: models.Product = serialize_result.model
    new_product.user_id = flask.g.client_id

    # save the image file to the server
    _updateImage(new_product)
    
    # using the product's repository, insert the product into the database
    repository_result = proudcts_repo.insert(new_product)

    if not repository_result.successful:
        return responses.badRequest(repository_result.error)
    
    return responses.created(new_product)

#------------------------------------------------------
# Update the product's image property if one was included
#
# Returns a bool:
#   true: image was updated
#   false: image was NOT updated (included)
#------------------------------------------------------
def _updateImage(product: models.Product) -> bool:
    # set the image if one was uploaded
    product_image_file = flask.request.files.get('image')

    if not product_image_file:
        return False

    # get the cover photos directory on the server
    cover_photos_directory = user_image.getCoverDirectory()

    product.image = _setImagePropertyFromImageFile(product_image_file, cover_photos_directory)

    return True

#------------------------------------------------------
# takes a raw image file, saves it locally, and sets the image field in the database to the image file name as saved on the server
#
# parms:
#   new_image_file - the raw image file
#   relative_image_directory_path - the folder name to save the image to
#
# Returns the Product's new image file name to save into the database
#------------------------------------------------------
def _setImagePropertyFromImageFile(new_image_file: object, relative_image_directory_path: str) -> str:
    # remove the old image
    # if self.image:
        # os.remove(os.path.join(relative_image_directory_path, self.image))

    # take the client provided cover photo and rename it using a unique UUID file name
    product_image = common.UserImage(new_image_file)
    new_image_file_name = utilities.getUUID(True) + product_image.getFileExtension()

    # save the renamed file onto the server and fetch the new file's name
    return product_image.saveImageFile(relative_image_directory_path, new_image_file_name)



