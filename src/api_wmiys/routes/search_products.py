"""
Package:        search_products
Url Prefix:     /search/products/
Description:    Handles all the product search routing.
"""
from functools import wraps, update_wrapper
import flask
from flask import Blueprint, jsonify, request
from ..db import DB
from ..common import security, SortingSearchProducts, Pagination
from ..models import ProductSearchRequest


searchProducts = Blueprint('searchProducts', __name__)

# module variables to store request parms
m_sorting = SortingSearchProducts(SortingSearchProducts.ACCEPTABLE_FIELDS, 'name')
m_pagination = Pagination()
m_requestParms = ProductSearchRequest(oSorting=m_sorting, oPagination=m_pagination)


#-----------------------------------------------------
# DECORATORS
# ----------------------------------------------------
def init_module_members(f):
    """Calls all the necessary functions prior to the request.

    - Make sure the required request query parms are set
    - Store the required query parms
    - setup the sorting object
    - setup the pagination object
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        initRequiredQueryParms()
        initSorting()
        initPagination()

        return f(*args, **kwargs)

    return wrap



#-----------------------------------------------------
# ROUTES
# ----------------------------------------------------
@searchProducts.route('', methods=['GET'])
@security.login_required
@init_module_members
def searchAll():
    searchResults, totalRows = m_requestParms.searchAll()
    return paginationReturnTemplate(searchResults, totalRows)


@searchProducts.route('categories/major/<int:product_categories_major_id>', methods=['GET'])
@security.login_required
@init_module_members
def searchProductCategoriesMajor(product_categories_major_id):
    searchResults, totalRows = m_requestParms.searchCategoriesMajor(product_categories_major_id)
    return paginationReturnTemplate(searchResults, totalRows)


@searchProducts.route('categories/minor/<int:product_categories_minor_id>', methods=['GET'])
@security.login_required
@init_module_members
def searchProductCategoriesMinor(product_categories_minor_id):
    searchResults, totalRows = m_requestParms.searchCategoriesMinor(product_categories_minor_id)
    return paginationReturnTemplate(searchResults, totalRows)

@searchProducts.route('categories/sub/<int:product_categories_sub_id>', methods=['GET'])
@security.login_required
@init_module_members
def searchProductCategoriesSub(product_categories_sub_id):
    searchResults, totalRows = m_requestParms.searchCategoriesSub(product_categories_sub_id)
    return paginationReturnTemplate(searchResults, totalRows)




#-----------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------
def initRequiredQueryParms():
    """Checks to make sure all the url query parameters are set.
    If they are set, then load them into the m_searchRequest module variable.
    Otherwise, send a 400 response.
    """
    global m_requestParms
    m_requestParms.location_id = request.args.get('location_id')
    m_requestParms.starts_on   = request.args.get('starts_on')
    m_requestParms.ends_on     = request.args.get('ends_on')

    
    if not m_requestParms.areRequiredPropertiesSet():
        flask.abort(400)    # not all of the properties were specified in the url


def initSorting():
    """Setup the sorting module object fields
    """
    global m_sorting

    if request.args.get('sort'):
        m_sorting.parse_sort_query(request.args.get('sort'))
    
    global m_requestParms
    m_requestParms.sorting = m_sorting


def initPagination():
    """Setup the sorting module object fields
    """
    global m_pagination        
    m_pagination.page = request.args.get('page') or Pagination.DEFAULT_PAGE
    m_pagination.per_page = request.args.get('per_page') or Pagination.DEFAULT_PER_PAGE

    global m_requestParms
    m_requestParms.pagination = m_pagination


def paginationReturnTemplate(searchResults, totalRows):
    return jsonify(results=searchResults, pagination=m_requestParms.pagination.getPaginationResponse(totalRows))






