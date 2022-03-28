"""
Package:        search_products
Url Prefix:     /search/products/
Description:    Handles all the product search routing.
"""
from functools import wraps
import flask
from http import HTTPStatus
from ..common import security, SortingSearchProducts, Pagination
from ..models import ProductSearchRequest, FilterCategories


from api_wmiys.services import search_products as search_products_services


# Flask blueprint
bp_search_products = flask.Blueprint('searchProducts', __name__)

# module variables to store request parms
m_sorting = SortingSearchProducts(SortingSearchProducts.ACCEPTABLE_FIELDS, 'name')
m_pagination = Pagination()
m_requestParms = ProductSearchRequest(sorting=m_sorting, pagination=m_pagination)


#-----------------------------------------------------
# Decorator function that calls all the necessary setup
# functions prior to the request:
#   - Make sure the required request query parms are set
#   - Store the required query parms
#   - setup the sorting object
#   - setup the pagination object
# ----------------------------------------------------
def init_module_members(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        initRequiredQueryParms()
        initSorting()
        initPagination()

        return f(*args, **kwargs)

    return wrap


#-----------------------------------------------------
# Seach all
# ----------------------------------------------------
@bp_search_products.get('')
@security.login_required
@init_module_members
def searchAll():
    return search_products_services.respones_GET_ALL()

    searchResults, totalRows = m_requestParms.searchAll()
    return paginationReturnTemplate(searchResults, totalRows)


#-----------------------------------------------------
# Seach major categories
# ----------------------------------------------------
@bp_search_products.get('categories/major/<int:product_categories_major_id>')
@security.login_required
@init_module_members
def searchProductCategoriesMajor(product_categories_major_id):
    searchResults, totalRows = m_requestParms.searchCategories(FilterCategories.MAJOR, product_categories_major_id)
    return paginationReturnTemplate(searchResults, totalRows)


#-----------------------------------------------------
# Seach minor categories
# ----------------------------------------------------
@bp_search_products.get('categories/minor/<int:product_categories_minor_id>')
@security.login_required
@init_module_members
def searchProductCategoriesMinor(product_categories_minor_id):
    searchResults, totalRows = m_requestParms.searchCategories(FilterCategories.MINOR, product_categories_minor_id)
    return paginationReturnTemplate(searchResults, totalRows)

#-----------------------------------------------------
# Seach sub categories
# ----------------------------------------------------
@bp_search_products.get('categories/sub/<int:product_categories_sub_id>')
@security.login_required
@init_module_members
def searchProductCategoriesSub(product_categories_sub_id):
    searchResults, totalRows = m_requestParms.searchCategories(FilterCategories.SUB, product_categories_sub_id)
    return paginationReturnTemplate(searchResults, totalRows)




#-----------------------------------------------------
# Checks to make sure all the url query parameters are set.
# If they are set, then load them into the m_searchRequest module variable.
# Otherwise, send a 400 response.
# ----------------------------------------------------
def initRequiredQueryParms():
    global m_requestParms
    m_requestParms.location_id = flask.request.args.get('location_id')
    m_requestParms.starts_on   = flask.request.args.get('starts_on')
    m_requestParms.ends_on     = flask.request.args.get('ends_on')

    if not m_requestParms.areRequiredPropertiesSet():
        # not all of the properties were specified in the url
        flask.abort(HTTPStatus.BAD_REQUEST.value)    

#-----------------------------------------------------
# Setup the sorting module object fields
# ----------------------------------------------------
def initSorting():
    global m_sorting

    if flask.request.args.get('sort'):
        m_sorting.parse_sort_query(flask.request.args.get('sort'))
    
    global m_requestParms
    m_requestParms.sorting = m_sorting

#-----------------------------------------------------
# Setup the pagination module object fields
# ----------------------------------------------------
def initPagination():
    global m_pagination
    m_pagination.page = flask.request.args.get('page') or Pagination.DEFAULT_PAGE
    m_pagination.per_page = flask.request.args.get('per_page') or Pagination.DEFAULT_PER_PAGE

    global m_requestParms
    m_requestParms.pagination = m_pagination

#-----------------------------------------------------
# helper function to return the pagination and results
# ----------------------------------------------------
def paginationReturnTemplate(searchResults, totalRows):
    return flask.jsonify(results=searchResults, pagination=m_requestParms.pagination.getPaginationResponse(totalRows))






