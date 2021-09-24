"""
Package:        product_listings
Url Prefix:     /listings/<int:product_id>
Description:    Handles all the product listings routing.
"""

import flask
from ..common import security
from ..models import ProductListing, ProductListingAvailability


productListings = flask.Blueprint('productListings', __name__)

@productListings.route('', methods=['GET'])
@security.login_required
def getProductListings(product_id: int):
    listing = ProductListing(product_id)
    return flask.jsonify(listing.get())


@productListings.route('availability', methods=['GET'])
@security.login_required
def getProductListingAvailability(product_id: int):
    listingAvailability = ProductListingAvailability(product_id=product_id)
    listingAvailability.location_id = flask.request.args.get('location_id')
    listingAvailability.starts_on = flask.request.args.get('starts_on')
    listingAvailability.ends_on = flask.request.args.get('ends_on')

    # be sure all 3 required query parms have a non-None value
    if not listingAvailability.areAllPropertiesSet():
        return ('Missing a required property', 400)
    
    responseDict = dict(available=listingAvailability.isProductAvailable())
    
    return flask.jsonify(responseDict)





