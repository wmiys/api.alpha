"""
Package:        products
Url Prefix:     /products
Description:    Handles all the products routing.
"""

import flask
from ..common import security
from ..services import products as products_service
from ..common import responses

bp_products = flask.Blueprint('products', __name__)

#------------------------------------------------------
# Create a new product or fetch all of a user's products
#------------------------------------------------------
@bp_products.route('', methods=['GET', 'POST'])
@security.login_required
def noID():

    if flask.request.method == 'POST':
        return products_service.post()         # Create a new product
    else:
        return responses.get(output = products_service.getAll())


#------------------------------------------------------
# Retrieve or update an existing product
#------------------------------------------------------
@bp_products.route('<int:product_id>', methods=['GET', 'PUT'])
@security.login_required
def productRequest(product_id):
    
    if flask.request.method == 'PUT':
        return products_service.put(product_id)
    else:
        return products_service.get(product_id)
            
        
