"""
Package:        search
Url Prefix:     /search
Description:    Handles all the search routing.
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from api_wmiys.DB.DB import DB


search = Blueprint('search', __name__)


@search.route('locations', methods=['GET'])
def searchLocations():
    """Search for locations
    """
    query = request.args.get('q')

    # make sure the q argumrnt is set by the client
    if query == None:
        flask.abort(400)

    # if no per_page argument was given or it's gt 100, set it to the default (20)
    per_page = request.args.get('per_page')
    if per_page == None or int(per_page) > 100:
        per_page = 20
    
    search_results = DB.searchLocations(query=query, num_results=per_page)

    return jsonify(search_results)