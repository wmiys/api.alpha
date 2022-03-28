
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import flask


# from ..models import ProductSearchRequest, FilterCategories
from wmiys_common import utilities

from api_wmiys.common import SortingSearchProducts
from api_wmiys.common.pagination import getRequestPaginationParms
from api_wmiys.common import responses
from api_wmiys.common.base_return import FilteredDataReturn
from api_wmiys.domain import models
from api_wmiys.repository import search_products as search_products_repo


#-----------------------------------------------------
# Seach all
# ----------------------------------------------------
def respones_GET_ALL() -> flask.Response:
    # gather the request url query parms
    request_parms = _getProductSearchRequest()

    # make sure all of the required ones are provided by the client
    if not _areRequiredParmsSet(request_parms):
        return responses.badRequest('Missing a required url query paramter.')

    repo_result = _getAll(request_parms)

    return _returnFilteredDataResult(repo_result)



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
# Get all the product records and the pagination counts
#-----------------------------------------------------
def _getAll(product_search_request: models.ProductSearchRequest) -> FilteredDataReturn:
    result = FilteredDataReturn(successful=True)
    
    try:
        result.data          = _getAllRecords(product_search_request)
        result.count_records = _getAllTotalRecordCount(product_search_request)
        result.count_pages   = product_search_request.pagination.totalPages(result.count_records)
    
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
def _areRequiredParmsSet(parms: models.ProductSearchRequest) -> bool:
    if None in [parms.location_id, parms.starts_on, parms.ends_on]:
        return False
    else:
        return True


#-----------------------------------------------------
# Get all the filtered records from the repository
#-----------------------------------------------------
def _getAllRecords(product_search_request: models.ProductSearchRequest) -> list[dict]:
    # get the actual records
    db_result = search_products_repo.selectAll(product_search_request)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data or []
        
#-----------------------------------------------------
# Get the total record count from the repository
#-----------------------------------------------------
def _getAllTotalRecordCount(product_search_request: models.ProductSearchRequest) -> int:
    db_result = search_products_repo.selectAllTotalCount(product_search_request)

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
        





def respones_GET_MAJOR(product_categories_major_id) -> flask.Response:
    return 'respones_GET_MAJOR'


def respones_GET_MINOR(product_categories_minor_id) -> flask.Response:
    return 'respones_GET_MINOR'


def respones_GET_SUB(product_categories_sub_id) -> flask.Response:
    return 'respones_GET_SUB'


