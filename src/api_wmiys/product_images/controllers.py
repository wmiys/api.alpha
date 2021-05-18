"""
Package:        product_images
Url Prefix:     /users/<int:user_id>/products/<int:product_id>/images
Description:    Handles all the product images routing
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from api_wmiys.DB.DB import DB

productImages = Blueprint('productImages', __name__)


#-----------------------------------------------------
# ROUTES
# ----------------------------------------------------
@productImages.route('', methods=['GET'])
# @Security.login_required
# @init_module_members
def searchAll(user_id: int, product_id: int):
    return 'Product images blueprint'