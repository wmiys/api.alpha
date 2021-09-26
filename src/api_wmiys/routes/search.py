"""
Package:        search
Url Prefix:     /search
Description:    Handles all the search routing.
"""
from __future__ import annotations
import flask
from flask import Blueprint
from ..db import DB


DEFAULT_PER_PAGE_VALUE = 20
MAX_PER_PAGE_VALUE = 100

search = Blueprint('search', __name__)


#------------------------------------------------------
# Location search url routing logic
#------------------------------------------------------
@search.route('locations', methods=['GET'])
def searchLocations():
    query = getQuery()
    per_page = getPerPage()
    search_results = searchLocations(query=query, num_results=per_page)

    return flask.jsonify(search_results)


#------------------------------------------------------
# Retrieve the query ('q') url parm.
# The query parm is required, so if it's missing respond with a 400
#------------------------------------------------------
def getQuery():
    query = flask.request.args.get('q')

    if query == None:
        flask.abort(400)

    return query

#------------------------------------------------------
# Get the per_page ('per_page') url parm
#
# The result is set to the default if:
#   - the parm is not provided in the url
#   - the value is greater than 100
#   - the value is less than 1
#------------------------------------------------------
def getPerPage() -> int:
    per_page = flask.request.args.get('per_page') or None
    
    if not per_page:
        return DEFAULT_PER_PAGE_VALUE
    elif int(per_page) > MAX_PER_PAGE_VALUE:
        return DEFAULT_PER_PAGE_VALUE
    elif int(per_page) < 1:
        return DEFAULT_PER_PAGE_VALUE
    else:
        return int(per_page)

#------------------------------------------------------
# Call the search location sql stored procedure
#
# Parms:
#   query - location search query
#   num_results - the number of search results to return
#
# Returns: a list of dictionaries
#------------------------------------------------------
def searchLocations(query: str, num_results: int) -> list[dict]:
        db = DB()
        db.connect()
        mycursor = db.getCursor(True)

        parms = [query, num_results]
        result_args = mycursor.callproc('Search_Locations', parms)
        locations_record_set = next(mycursor.stored_results())
        
        db.close()

        return locations_record_set