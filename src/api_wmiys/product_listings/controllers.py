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



productListings = Blueprint('productListings', __name__)

@productListings.route('', methods=['GET'])
@Security.login_required
def getProductListings(product_id: int):
    listing = ProductListing(product_id)

    return jsonify(listing.get())





