"""
Package:        product_images
Url Prefix:     /products/<int:product_id>/images
Description:    Handles all the product images routing
"""

import flask
from flask import Blueprint, jsonify, request
from ..common import security
from ..models import ProductImage, product

bpProductImages = Blueprint('bpProductImages', __name__)


#-----------------------------------------------------
# Access/modify the images for a single product
# ----------------------------------------------------
@bpProductImages.route('', methods=['GET', 'POST', 'DELETE'])
@security.login_required
def searchAll(product_id: int):
    # make sure the user is authorized
    if not product.doesUserOwnProduct(product_id, security.requestGlobals.client_id):
        return ('', 403)

    if request.method == 'GET':
        return jsonify(ProductImage.getAll(product_id))     # all we need to do is fetch all the product images      
    elif request.method == 'DELETE':
        ProductImage.deleteAll(product_id)
        return ('', 200)
    
    # if we get to this point, we are creating a new product image record
    imagesData = dict(request.files.to_dict())

    for img in imagesData.values():
        productImage = ProductImage(product_id=product_id)
        productImage.setImagePropertyFromImageFile(img, ProductImage.LOCAL_SERVER_IMAGE_DIRECTORY_RELATIVE)
        productImage.insert()

    
    return jsonify(ProductImage.getAll(product_id))


#----------------------------------------------------------
# Get a single product image
#----------------------------------------------------------
@bpProductImages.route('<int:product_image_id>', methods=['GET'])
@security.login_required
def singleImage(product_id: int, product_image_id: int):
    # make sure the user is authorized
    if not product.doesUserOwnProduct(product_id, security.requestGlobals.client_id):
        return ('', 403)

    productImage = ProductImage(newID=product_image_id)    
    
    if not productImage.load():
        return ('', 400)

    return jsonify(productImage.toDict())


