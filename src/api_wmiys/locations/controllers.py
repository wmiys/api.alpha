"""
Package:        locations
Url Prefix:     /locations/
Description:    Routing for locations
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
# from api_wmiys.product_listings.ProductListing import ProductListing
from api_wmiys.locations.Location import Location


locationsBP = Blueprint('locationsBP', __name__)

@locationsBP.route('<int:location_id>', methods=['GET'])
@Security.login_required
def getLocations(location_id: int):
    location = Location(location_id)
    location.load()

    return jsonify(location.toDict())
