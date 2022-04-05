"""
Package:        search
Url Prefix:     /search
Description:    Handles all the search routing.
"""

from __future__ import annotations
import flask
from api_wmiys.services import search_locations as search_locations_services

bp_search = flask.Blueprint('search', __name__)


#------------------------------------------------------
# Location search url routing logic
#------------------------------------------------------
@bp_search.get('locations')
def _searchLocations():
    return search_locations_services.responses_GET_ALL()
