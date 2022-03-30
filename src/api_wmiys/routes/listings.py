"""
Package:        product_listings
Url Prefix:     /listings/<int:product_id>
Description:    Handles all the product listings routing.
"""

import flask
from http import HTTPStatus
from api_wmiys.common import security
from ..models import ProductListingAvailability

from api_wmiys.services import listings as listing_services


bp_listings = flask.Blueprint('productListings', __name__)


#----------------------------------------------------------
# Get a product's listing information for a single product
#----------------------------------------------------------
@bp_listings.get('')
@security.login_required
def getProductListings(product_id: int):
    return listing_services.responses_GET(product_id)


#----------------------------------------------------------
# Check if a product is available for rent
#----------------------------------------------------------
@bp_listings.get('availability')
@security.login_required
def getProductListingAvailability(product_id: int):
    listingAvailability = ProductListingAvailability(
        product_id  = product_id,
        location_id = flask.request.args.get('location_id'),
        starts_on   = flask.request.args.get('starts_on'),
        ends_on     = flask.request.args.get('ends_on'),
    )

    # be sure all 3 required query parms have a non-None value
    if not listingAvailability.areAllPropertiesSet():
        return ('Missing a required property', HTTPStatus.BAD_REQUEST.value)
    
    responseDict = dict(available=listingAvailability.isProductAvailable())
    
    return flask.jsonify(responseDict)





