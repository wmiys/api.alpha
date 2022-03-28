

from dataclasses import dataclass
from datetime import date
import flask


# from ..models import ProductSearchRequest, FilterCategories


from api_wmiys.models import ProductRequest
from api_wmiys.models import FilterCategories
from api_wmiys.common import SortingSearchProducts
from api_wmiys.common import Pagination
from api_wmiys.common.pagination import getRequestPaginationParms
from api_wmiys.common import responses


@dataclass
class SearchProductsUrlParms:
    location_id : int                   = None
    starts_on   : date                  = None
    ends_on     : date                  = None
    pagination  : Pagination            = None
    sorting     : SortingSearchProducts = None



def respones_GET_ALL() -> flask.Response:
    
    request_parms = getRequestQueryParms()

    if not areRequiredParmsSet(request_parms):
        return responses.badRequest('Missing a required url query paramter.')
    

    
    
    return 'get all'





def getRequestQueryParms() -> SearchProductsUrlParms:

    result = SearchProductsUrlParms(
        location_id = flask.request.args.get('location_id') or None,
        starts_on   = date.fromisoformat(flask.request.args.get('starts_on')) or None,
        ends_on     = date.fromisoformat(flask.request.args.get('ends_on')) or None,
        pagination = getRequestPaginationParms(),

    )

    return result








def areRequiredParmsSet(parms: SearchProductsUrlParms) -> bool:
    if None in [parms.location_id, parms.starts_on, parms.ends_on]:
        return False
    else:
        return True






















def respones_GET_MAJOR(product_categories_major_id) -> flask.Response:
    return 'respones_GET_MAJOR'


def respones_GET_MINOR(product_categories_minor_id) -> flask.Response:
    return 'respones_GET_MINOR'


def respones_GET_SUB(product_categories_sub_id) -> flask.Response:
    return 'respones_GET_SUB'


