"""
Package:        product_images
Url Prefix:     /products/<int:product_id>/images
Description:    Handles all the product images routing
"""

import flask
from http import HTTPStatus
from api_wmiys.common import user_image
from ..common import security
from ..models import product_image, ProductImage

bp_product_images = flask.Blueprint('bpProductImages', __name__)


#-----------------------------------------------------
# GET the images for a product
# Just fetch all the product images
# ----------------------------------------------------
@bp_product_images.get('')
@security.login_required
def get(product_id: int):
    return flask.jsonify(product_image.getAll(product_id))


#-----------------------------------------------------
# DELETE the images for a product
# ----------------------------------------------------
@bp_product_images.delete('')
@security.login_required
@security.verify_product_owner
def delete(product_id):    
    product_image.deleteAll(product_id)

    return ('', HTTPStatus.NO_CONTENT.value)


#-----------------------------------------------------
# POST the images for a product
# ----------------------------------------------------
@bp_product_images.post('')
@security.login_required
@security.verify_product_owner
def post(product_id):    
    images_data: dict = flask.request.files.to_dict()
    directory_path = user_image.getImagesDirectory()

    for img in images_data.values():
        productImage = ProductImage(product_id=product_id)
        productImage.setImagePropertyFromImageFile(img, directory_path)
        productImage.insert()

    return flask.jsonify(product_image.getAll(product_id))


#----------------------------------------------------------
# Get a single product image
#----------------------------------------------------------
@bp_product_images.get('<int:product_image_id>')
@security.login_required
@security.verify_product_owner
def singleImage(product_id, product_image_id: int):
    product_image = ProductImage(newID=product_image_id)    
    
    if not product_image.load():
        return ('', HTTPStatus.BAD_REQUEST.value)

    return flask.jsonify(product_image.toDict())


