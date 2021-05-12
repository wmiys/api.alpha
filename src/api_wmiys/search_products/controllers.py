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
from api_wmiys.common.Pagination import Pagination
from functools import wraps, update_wrapper

searchProducts = Blueprint('searchProducts', __name__)
m_requestParms = ProductSearchRequest()
m_sorting = SortingSearchProducts(SortingSearchProducts.ACCEPTABLE_FIELDS, 'name')
m_pagination = Pagination()


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

def init_pagination(f):
    """Setup the sorting module object fields
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        global m_pagination

        if request.args.get('page'):
            m_pagination.page = request.args.get('page')            
        else:
            m_pagination.page = Pagination.DEFAULT_PAGE
        
        if request.args.get('per_page'):
            m_pagination.per_page = request.args.get('per_page')
        else:
            m_pagination.per_page = Pagination.DEFAULT_PER_PAGE
        
        global m_requestParms
        m_requestParms.pagination = m_pagination

        return f(*args, **kwargs)

    return wrap


@searchProducts.route('', methods=['GET'])
@Security.login_required
@init_query
@init_sorting
@init_pagination
def searchAll():
    searchResults, totalRows = m_requestParms.searchAll()
    
    return jsonify(totalRows=totalRows, pagination=m_pagination.to_dict(), searchResults=searchResults)


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


