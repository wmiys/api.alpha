"""
**********************************************************************************************

Application logic for products.

**********************************************************************************************
"""

from __future__ import annotations

import flask

from pymysql.structs import DbOperationResult
from wmiys_common import utilities

from .. import common
from api_wmiys.repository import products as proudcts_repo
from api_wmiys.domain import models
from api_wmiys.common import serializers


#------------------------------------------------------
# Responsd to a GET all request
#------------------------------------------------------
def response_GET_ALL() -> flask.Response:
    products = getAllProducts()
    return common.responses.get(products)

#------------------------------------------------------
# Retrieve all the user's products
#------------------------------------------------------
def getAllProducts() -> list[dict]:
    products = proudcts_repo.selectAll(flask.g.client_id).data or []

    for product in products:
        _setImageUrlPrefix(product)

    return products

#------------------------------------------------------
# Update an existing product
#------------------------------------------------------
def response_PUT(product_id) -> flask.Response:
    # serialize the incoming form data into a Product domain model
    product_to_update = extractFormData(product_id)

    # save the image file to the server
    _updateImage(product_to_update)

    # send the product domain model to the repository to record the updates in the database
    db_result = proudcts_repo.update(product_to_update)
    
    if not db_result.successful:
        return common.responses.badRequest(str(db_result.error))
    
    # now, fetch the product from the database to get its updated data and to make sure the user owns it
    return _standardSingleProductReturn(product_id, common.responses.updated)

#------------------------------------------------------
# Create a new product
#------------------------------------------------------
def response_POST() -> flask.Response:
    # fetch the incoming request data dict
    new_product = extractFormData()

    # save the image file to the server
    _updateImage(new_product)
    
    # using the product's repository, insert the product into the database
    repository_result = proudcts_repo.insert(new_product)

    if not repository_result.successful:
        return common.responses.badRequest(repository_result.error)

    # now return the newly created product
    return _standardSingleProductReturn(new_product.id, common.responses.created)


#------------------------------------------------------
# Retrieve a single product
#------------------------------------------------------
def response_GET(product_id) -> flask.Response:
    return _standardSingleProductReturn(product_id, common.responses.get)


#------------------------------------------------------
# Gather the incoming flask request data
# Serialize it into a Product domain model
# Explicitly set the Product's id and user_id
#------------------------------------------------------
def extractFormData(product_id: int = None) -> models.Product:
    # get a Product domain model with all of it's database values set to its attributes
    # this is so that for an update, it won't override missing fields in the request
    existing_product = getProductModel(product_id, flask.g.client_id)

    # serialize the incoming form data into a Product domain model
    form = flask.request.form.to_dict()
    serializer = serializers.ProductSerializer(form, existing_product)
    product = serializer.serialize().model

    # Explicitly set the product's id and user_id
    # Just in case the client provided an id or user_ud field in the form data
    product.id = product_id
    product.user_id = flask.g.client_id

    return product


#------------------------------------------------------
# Fetch a Product record from the database that matches the given id 
# And, return a flask.Response using the given responses callback.
#
# Args:
#     product_id: the Product's id
#     responses_callback: a common.responses callback method
#    
# Returns:
#     a flask.Response to return to the client
#------------------------------------------------------
def _standardSingleProductReturn(product_id, responses_callback) -> flask.Response:
    db_result = getProductView(product_id, flask.g.client_id)

    if not db_result.successful:
        return common.responses.badRequest(str(db_result.error))
    
    # client does not own the data or it does not exist
    if not db_result.data:
        return common.responses.notFound()
    
    _setImageUrlPrefix(db_result.data)

    return responses_callback(db_result.data)

#------------------------------------------------------
# Prepend the absolute image file path to each image field, if one exists
#------------------------------------------------------
def _setImageUrlPrefix(product_dict: dict):
    if product_dict['image']:
        prefix = common.user_image.getCoverUrl()
        product_dict['image'] = prefix + product_dict['image']

#------------------------------------------------------
# Update the product's image property if one was included
#
# Returns a bool:
#   true: image was updated
#   false: image was NOT updated (included)
#------------------------------------------------------
def _updateImage(product: models.Product) -> bool:
    # set the product's image value to the existing one
    existing_product = getProductModel(product.id, product.user_id)

    if not existing_product:
        return False

    product.image = existing_product.image
    
    # set the image if one was uploaded
    product_image_file = flask.request.files.get('image')

    if not product_image_file:
        return False

    # get the cover photos directory on the server
    cover_photos_directory = common.user_image.getCoverDirectory()

    product.image = _setImagePropertyFromImageFile(product_image_file, cover_photos_directory)

    return True


#------------------------------------------------------
# Verifies that the given product is owned by the given user.
#
# Parms:
#   product_id: the product's id
#   user_id: the user's id
#
# Returns a bool:
#   true - user owns the product
#   false - user DOES NOT own the product
#------------------------------------------------------
def doesUserOwnProduct(product_id: int, user_id: int) -> bool:
    product = getProductModel(product_id, user_id)

    if not product:
        return False
    else:
        return True



#------------------------------------------------------
# Fetch a product with the given id/user_id combination
#
# Returns a DbOperationResult
#------------------------------------------------------
def getProductView(product_id: int, user_id: int) -> DbOperationResult:
    product = models.Product(
        id      = product_id,
        user_id = user_id,
    )

    db_result = proudcts_repo.select(product)

    return db_result

#------------------------------------------------------
# Get a Product domain model given its id and user_id
#------------------------------------------------------
def getProductModel(product_id, user_id) -> models.Product | None:
    product_shell = models.Product(
        id = product_id,
        user_id = user_id,
    )

    select_result = proudcts_repo.select(product_shell).data

    if not select_result:
        return None

    serialization_result = serializers.ProductSerializer(select_result).serialize()

    return serialization_result.model


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




