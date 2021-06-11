"""
Package:        product_listings
Url Prefix:     /listings/<int:product_id>
Description:    Handles all the product listings routing.
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from api_wmiys.product_listings.ProductListing import ProductListing
from api_wmiys.product_listings.ProductListingAvailability import ProductListingAvailability

productListings = Blueprint('productListings', __name__)

@productListings.route('', methods=['GET'])
@Security.login_required
def getProductListings(product_id: int):
    listing = ProductListing(product_id)
    return jsonify(listing.get())


@productListings.route('availability', methods=['GET'])
@Security.login_required
def getProductListingAvailability(product_id: int):
    listingAvailability = ProductListingAvailability(product_id=product_id)
    listingAvailability.location_id = request.args.get('location_id')
    listingAvailability.starts_on = request.args.get('starts_on')
    listingAvailability.ends_on = request.args.get('ends_on')

    # be sure all 3 required query parms have a non-None value
    if not listingAvailability.areAllPropertiesSet():
        return ('Missing a required property', 400)
    
    responseDict = dict(available=listingAvailability.isProductAvailable())
    
    return jsonify(responseDict)





