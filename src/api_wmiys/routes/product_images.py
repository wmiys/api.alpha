"""
Package:        product_images
Url Prefix:     /products/<int:product_id>/images
Description:    Handles all the product images routing
"""

import flask
from api_wmiys.common import security
from api_wmiys.services import product_images as product_image_services


bp_product_images = flask.Blueprint('bpProductImages', __name__)


#-----------------------------------------------------
# GET the images for a product
# Just fetch all the product images
# ----------------------------------------------------
@bp_product_images.get('')
@security.login_required
def get(product_id: int):
    return product_image_services.responses_GET_ALL(product_id)


#-----------------------------------------------------
# DELETE the images for a product
# ----------------------------------------------------
@bp_product_images.delete('')
@security.login_required
@security.verify_product_owner
def delete(product_id):    
    return product_image_services.responses_DELETE_ALL(product_id)


#-----------------------------------------------------
# POST the images for a product
# ----------------------------------------------------
@bp_product_images.post('')
@security.login_required
@security.verify_product_owner
def post(product_id):    
    return product_image_services.responses_POST(product_id)


