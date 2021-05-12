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
from api_wmiys.search_products.ProductSearchRequest import ProductSearchRequest
from api_wmiys.common.Sorting import SortingSearchProducts
from functools import wraps, update_wrapper

searchProducts = Blueprint('searchProducts', __name__)
m_requestParms = ProductSearchRequest()
m_sorting = SortingSearchProducts(SortingSearchProducts.ACCEPTABLE_FIELDS, 'name')


def init_query(f):
    """Checks to make sure all the url query parameters are set.

    If they are set, then load them into the m_searchRequest module variable.

    Otherwise, send a 400 response.
    """
    @wraps(f)
    def wrap(*args, **kwargs):

        global m_requestParms
        m_requestParms.location_id = request.args.get('location_id')
        m_requestParms.starts_on   = request.args.get('starts_on')
        m_requestParms.ends_on     = request.args.get('ends_on')

        if not m_requestParms.areRequiredPropertiesSet():
            flask.abort(400)    # not all of the properties were specified in the url

        return f(*args, **kwargs)

    return wrap

def init_sorting(f):
    """Setup the sorting module object fields
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        global m_sorting

        if request.args.get('sort'):
            m_sorting.parse_sort_query(request.args.get('sort'))
        
        global m_requestParms
        m_requestParms.sorting = m_sorting

        return f(*args, **kwargs)

    return wrap


@searchProducts.route('', methods=['GET'])
@Security.login_required
@init_query
@init_sorting
def searchAll():
    # searchResult = m_requestParms.searchAll()
    searchResult = m_requestParms.searchAll()
    return jsonify(searchResult)


@searchProducts.route('categories/major/<int:product_categories_major_id>', methods=['GET'])
@init_query
@Security.login_required
@init_sorting
def searchProductCategoriesMajor(product_categories_major_id):
    searchResult = m_requestParms.searchCategoriesMajor(product_categories_major_id)
    return jsonify(searchResult)


@searchProducts.route('categories/minor/<int:product_categories_minor_id>', methods=['GET'])
@Security.login_required
@init_query
@init_sorting
def searchProductCategoriesMinor(product_categories_minor_id):
    searchResult = m_requestParms.searchCategoriesMinor(product_categories_minor_id)
    return jsonify(searchResult)

@searchProducts.route('categories/sub/<int:product_categories_sub_id>', methods=['GET'])
@Security.login_required
@init_query
@init_sorting
def searchProductCategoriesSub(product_categories_sub_id):
    searchResult = m_requestParms.searchCategoriesSub(product_categories_sub_id)

    return jsonify(searchResult)


