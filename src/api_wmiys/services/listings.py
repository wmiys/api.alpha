"""
**********************************************************************************************

- A product listing represents a product that is publicly visible to all renters. 
- This is what data is used when a renter goes to a product-listing page. 
- It's essentially the same thing as the product view from the lender's side.
- I just thought it would be a good idea to seperate out the views for security... might have been a mistake.

**********************************************************************************************
"""

from __future__ import annotations
import flask

from api_wmiys.repository import listings as listing_repo
from api_wmiys.common import responses
from api_wmiys.views import listings as listing_views
from api_wmiys.common import images as user_image

#----------------------------------------------------------
# Get a product's listing information for a single product
#----------------------------------------------------------
def responses_GET(product_id) -> flask.Response:
    try:
        view = getView(product_id)
    except Exception as ex:
        return responses.badRequest(str(ex))

    if not view:
        return responses.notFound()

    return responses.get(view)


#----------------------------------------------------------
# Get the Listing view object
#----------------------------------------------------------
def getView(product_id) -> listing_views.Listing | None:
    view_dict = _getViewDict(product_id)

    if not view_dict:
        return None

    listing_view = listing_views.Listing(
        meta       = _getViewMeta(view_dict),
        price      = _getViewPrice(view_dict),
        categories = _getViewCategories(view_dict),
        lender     = _getViewLender(view_dict),
    )

    return listing_view


#----------------------------------------------------------
# Fetch the view dictionary from the database
#----------------------------------------------------------
def _getViewDict(product_id) -> dict:
    result = listing_repo.select(product_id)

    if not result.successful:
        raise result.error

    return result.data

#----------------------------------------------------------
# Get the meta section of the Listing view
#----------------------------------------------------------
def _getViewMeta(view_dict: dict) -> listing_views.Meta:
    meta = listing_views.Meta(
        id          = view_dict.get('id') or None,
        name        = view_dict.get('name') or None,
        description = view_dict.get('description') or None,
        minimum_age = view_dict.get('minimum_age') or None,
        image       = view_dict.get('image') or None,
    )

    # prefix the image with the cover photo url
    if meta.image:
        directory = user_image.getCoverUrl()
        meta.image = f'{directory}{meta.image}'


    return meta

#----------------------------------------------------------
# Get the price section of the Listing view
#----------------------------------------------------------
def _getViewPrice(view_dict: dict) -> listing_views.Price:
    price_view = listing_views.Price(
        full = view_dict.get('price_full') or None,
    )

    return price_view

#----------------------------------------------------------
# Get the categories section of the Listing view
#----------------------------------------------------------
def _getViewCategories(view_dict: dict) -> listing_views.Categories:
    categories_view = listing_views.Categories(
        major_id   = view_dict.get('product_categories_major_id') or None,
        major_name = view_dict.get('product_categories_major_name') or None,
        minor_id   = view_dict.get('product_categories_minor_id') or None,
        minor_name = view_dict.get('product_categories_minor_name') or None,
        sub_id     = view_dict.get('product_categories_sub_id') or None,
        sub_name   = view_dict.get('product_categories_sub_name') or None,
    )

    return categories_view

#----------------------------------------------------------
# Get the lender section of the Listing view
#----------------------------------------------------------
def _getViewLender(view_dict: dict) -> listing_views.Lender:
    lender_view = listing_views.Lender(
        id         = view_dict.get('lender_id') or None,
        name_first = view_dict.get('lender_name_first') or None,
        name_last  = view_dict.get('lender_name_last') or None,
    )

    return lender_view
    

