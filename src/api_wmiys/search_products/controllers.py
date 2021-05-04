"""
Package:        search_products
Url Prefix:     /search/products/
Description:    Handles all the product search routing.
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from api_wmiys.DB.DB import DB
# import api_wmiys.DB.DB
from api_wmiys.search_products.ProductSearchRequest import ProductSearchRequest
from functools import wraps, update_wrapper

searchProducts = Blueprint('searchProducts', __name__)
m_searchRequest = ProductSearchRequest()

def init_query(f):
    """Checks to make sure all the url query parameters are set.

    If they are set, then load them into the m_searchRequest module variable.

    Otherwise, send a 400 response.
    """
    @wraps(f)
    def wrap(*args, **kwargs):

        global m_searchRequest
        m_searchRequest.location_id = request.args.get('location_id')
        m_searchRequest.starts_on   = request.args.get('starts_on')
        m_searchRequest.ends_on     = request.args.get('ends_on')

        if not m_searchRequest.areRequiredPropertiesSet():
            flask.abort(400)    # not all of the properties were specified in the url

        return f(*args, **kwargs)

    return wrap


@searchProducts.route('', methods=['GET'])
@Security.login_required
def userProductsGet():



    return 'Product search!'



@searchProducts.route('categories/sub/<int:product_categories_sub_id>', methods=['GET'])
@init_query
@Security.login_required
def searchProductCategoriesSub(product_categories_sub_id):

    searchResult = m_searchRequest.searchCategoriesSub(product_categories_sub_id)

    return jsonify(searchResult)


