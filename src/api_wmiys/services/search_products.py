"""
**********************************************************************************************
Doing a product search has a few steps involved since it utilizes pagination:
    - fetch a limited product record set using a LIMIT/OFFSET clause
    - fetch the total number of product records that would show up without the LIMIT/OFFSET clause.
        
The record count is needed becauase we need to calculate how many pages there are for the page_size.

For instance, let's say the product search results with no pagination would result in 75 records.
The incoming request url parms indicate that they would like the response to have 20 records per page.
The response would return that there are 4 total pages (1-4), 20 records (15 on the last) per page.
**********************************************************************************************
"""

from __future__ import annotations
from datetime import date
from functools import wraps

import flask

from api_wmiys.common import SortingSearchProducts
from api_wmiys.common import responses
from api_wmiys.common.pagination import getRequestPaginationParms
from api_wmiys.common.base_return import FilteredDataReturn
from api_wmiys.domain import models
from api_wmiys.domain.enums.product_categories import ColumnNames
from api_wmiys.domain.enums.product_categories import UrlCategoryNames
from api_wmiys.repository import search_products as search_products_repo

#-----------------------------------------------------
# Seach all major categories
# ----------------------------------------------------
def respones_GET_MAJOR(category_id) -> flask.Response:
    search_parms = _getProductSearchRequestCategory(ColumnNames.MAJOR, category_id)
    return _responsesTemplate(search_parms, _fetchCategory)

#-----------------------------------------------------
# Seach all minor categories
# ----------------------------------------------------
def respones_GET_MINOR(category_id) -> flask.Response:
    search_parms = _getProductSearchRequestCategory(ColumnNames.MINOR, category_id)
    return _responsesTemplate(search_parms, _fetchCategory)

#-----------------------------------------------------
# Seach all sub categories
# ----------------------------------------------------
def respones_GET_SUB(category_id) -> flask.Response:
    search_parms = _getProductSearchRequestCategory(ColumnNames.SUB, category_id)
    return _responsesTemplate(search_parms, _fetchCategory)


#-----------------------------------------------------
# Seach all
# ----------------------------------------------------
def respones_GET_ALL() -> flask.Response:
    request_parms = _getProductSearchRequest()
    return _responsesTemplate(request_parms, _fetch)

#-----------------------------------------------------
# Template for the responses routines to call
#-----------------------------------------------------
def _responsesTemplate(url_parms, get_all_callback) -> flask.Response:
    # make sure all of the required ones are provided by the client
    if not _areRequiredParmsSet(url_parms):
        return responses.badRequest('Missing a required url query paramter.')

    repo_result = get_all_callback(url_parms)

    return _returnFilteredDataResult(repo_result)

#-----------------------------------------------------
# Gather all the request url parms to filter out the search results for a category search
#-----------------------------------------------------
def _getProductSearchRequestCategory(category_type: ColumnNames, category_id: int) -> models.ProductSearchRequestCategory:
    # get the base ProductSearchRequest object with its values filled
    url_parms_base = _getProductSearchRequest()

    # copy over its values into a child ProductSearchRequestCategory object
    product_search_category = models.ProductSearchRequestCategory()
    product_search_category.__dict__.update(vars(url_parms_base))

    # set its category value
    product_search_category.category_type = category_type
    product_search_category.category_id = category_id

    return product_search_category

#-----------------------------------------------------
# Gather all the request url parms to filter out the search results
#-----------------------------------------------------
def _getProductSearchRequest() -> models.ProductSearchRequest:
    result = models.ProductSearchRequest(
        location_id = flask.request.args.get('location_id') or None,
        starts_on   = date.fromisoformat(flask.request.args.get('starts_on')) or None,
        ends_on     = date.fromisoformat(flask.request.args.get('ends_on')) or None,
        pagination  = getRequestPaginationParms(),
        sorting     = SortingSearchProducts(SortingSearchProducts.ACCEPTABLE_FIELDS, 'name'),
    )

    _setSortingUrlParmsValue(result)
    
    return result

#-----------------------------------------------------
# Set the given SearchProductsUrlParms's sorting value to the one found in the request's url
#-----------------------------------------------------
def _setSortingUrlParmsValue(url_parms: models.ProductSearchRequest):
    sort_url_value = flask.request.args.get('sort') or None

    if sort_url_value:
        url_parms.sorting.parse_sort_query(sort_url_value)

#-----------------------------------------------------
# Get all the product records and the pagination counts for all products
#-----------------------------------------------------
def _fetch(url_parms: models.ProductSearchRequest) -> FilteredDataReturn:
    return _fetchTemplate(url_parms, _fetchRecords, _fetchCount)


#-----------------------------------------------------
# Get all the product records and the pagination counts for a category
#-----------------------------------------------------
def _fetchCategory(url_parms: models.ProductSearchRequestCategory) -> FilteredDataReturn:
    return _fetchTemplate(url_parms, _fetchRecordsCategory, _fetchCountCategory)


#-----------------------------------------------------
# Template function for fetching both the data and pagination counts.
# 
# Args:
#     url_parms: either a ProductSearchRequest or ProductSearchRequestCategory
#     fetch_records_callback: callback for a fetch records routine
#     fetch_count_callback: fetch pagination count callback
#-----------------------------------------------------
def _fetchTemplate(url_parms, fetch_records_callback, fetch_count_callback) -> FilteredDataReturn:
    result = FilteredDataReturn(successful=True)
    
    try:
        result.data          = fetch_records_callback(url_parms)
        result.count_records = fetch_count_callback(url_parms)
        result.count_pages   = url_parms.pagination.totalPages(result.count_records)
    
    except Exception as e:
        result.successful    = False
        result.error         = e
        result.data          = None
        result.count_pages   = 0
        result.count_records = 0
        
    return result


#-----------------------------------------------------
# Verifiies that the client provided the required url parms in the request
#-----------------------------------------------------
def _areRequiredParmsSet(url_parms: models.ProductSearchRequest) -> bool:
    required_parms = [
        url_parms.location_id, 
        url_parms.starts_on, 
        url_parms.ends_on
    ]

    if None in required_parms:
        return False
    else:
        return True


#-----------------------------------------------------
# Get all the filtered records from the repository
#-----------------------------------------------------
def _fetchRecords(url_parms: models.ProductSearchRequest) -> list[dict]:
    return _fetchRecordsTemplate(url_parms, search_products_repo.selectAll)


#-----------------------------------------------------
# Get all the filtered records from the repository for a specific category
#-----------------------------------------------------
def _fetchRecordsCategory(url_parms: models.ProductSearchRequestCategory) -> list[dict]:
    return _fetchRecordsTemplate(url_parms, search_products_repo.selectAllCategory)

#-----------------------------------------------------
# Template for fetching the search product records.
# Returns an empty list if the db_result came back as null.
#-----------------------------------------------------
def _fetchRecordsTemplate(url_parms, repo_callback) -> list[dict]:
    # get the actual records
    db_result = repo_callback(url_parms)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data or []
        
#-----------------------------------------------------
# Get the total record count from the repository
#-----------------------------------------------------
def _fetchCount(url_parms: models.ProductSearchRequest) -> int:
    return _fetchCountTemplate(url_parms, search_products_repo.selectAllTotalCount)

#-----------------------------------------------------
# Get the total record count from the repository for a category
#-----------------------------------------------------
def _fetchCountCategory(url_parms: models.ProductSearchRequestCategory) -> int:
    return _fetchCountTemplate(url_parms, search_products_repo.selectAllCategoryTotalCount)

#-----------------------------------------------------
# Template for getting the total record count from the repository
#-----------------------------------------------------
def _fetchCountTemplate(url_parms, repository_callback) -> int:
    db_result = repository_callback(url_parms)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data.get('count') or 0


#-----------------------------------------------------
# Standaridized response generator for a FilteredDataReturn object
# All of the response functions should utilize this
#-----------------------------------------------------
def _returnFilteredDataResult(filtered_data: FilteredDataReturn) -> flask.Response:
    if not filtered_data.successful:
        return responses.badRequest(str(filtered_data.error))

    pagination_dict = dict(
        total_records = filtered_data.count_records,
        total_pages   = filtered_data.count_pages,
    )

    output = dict(
        pagination = pagination_dict,
        results    = filtered_data.data,
    )

    return responses.get(output)



#------------------------------------------------------
# Decorator for is_url_category_name_valid
#------------------------------------------------------
def validate_url_category_name(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        
        if not is_url_category_name_valid():
            return responses.notFound()

        return f(*args, **kwargs)
    return wrap

#------------------------------------------------------
# Make sure the url category_name value is valid 
#------------------------------------------------------
def is_url_category_name_valid() -> bool:
    category_name: str = flask.request.view_args.get('category_name') or None

    if not category_name:
        return False

    result = True

    try:
        UrlCategoryNames(category_name.lower())
    except ValueError as e:
        result = False

    return result


