"""
**********************************************************************************************
Services for searching for a location
**********************************************************************************************
"""

from __future__ import annotations
import flask
from api_wmiys.common import responses
from api_wmiys.domain import models
from api_wmiys.domain.enums.search_locations import PerPageLimits
from api_wmiys.repository import seach_locations as search_locations_repo

#------------------------------------------------------
# Location search url routing logic
#------------------------------------------------------
def responses_GET_ALL() -> flask.Response:
    url_parms = _getUrlQueryParms()

    # make sure the client provided a query in the url
    if not url_parms.query:
        return responses.badRequest(r"Missing required url query parm: 'q'")

    # execute the search
    try:
        location_views = _getAllViews(url_parms)
    except Exception as ex:
        return responses.badRequest(str(ex))
    
    return responses.get(location_views)


#------------------------------------------------------
# Get the url query parms from the request url
#------------------------------------------------------
def _getUrlQueryParms() -> models.SearchLocations:
    url_parms = models.SearchLocations(
        query    = _getQueryUrlParm(),
        per_page = _getPerPageUrlParm(),
    )

    return url_parms


#------------------------------------------------------
# Retrieve the query ('q') url parm.
#------------------------------------------------------
def _getQueryUrlParm() -> str | None:
    return flask.request.args.get('q') or None

#------------------------------------------------------
# Get the per page ('per_page') url parm
#
# The result is set to the default if:
#   - the parm is not provided in the url
#   - the value is greater than 100
#   - the value is less than 1
#------------------------------------------------------
def _getPerPageUrlParm() -> int:
    # get the per_page value from the url, or the default value if no parm was provided
    per_page = flask.request.args.get('per_page') or PerPageLimits.DEFAULT.value

    # if parsing it into an int does not work, just set it to the default
    try:
        per_page = int(per_page)
    except ValueError as e:
        per_page = PerPageLimits.DEFAULT.value

    # make sure the value is with in the range
    if PerPageLimits.MIN.value < per_page < PerPageLimits.MAX.value:
        per_page = PerPageLimits.DEFAULT.value
    
    return per_page


#------------------------------------------------------
# Fetch all the locations that fall within the search criteria
#------------------------------------------------------
def _getAllViews(url_parms: models.SearchLocations) -> list[dict]:
    db_result = search_locations_repo.selectAll(url_parms)

    if not db_result.successful:
        raise db_result.error
    
    return db_result.data or []

