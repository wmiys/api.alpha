"""
**********************************************************************************************
Package:        search_products
Url Prefix:     /search/products/
Description:    Handles all the product search routing.
**********************************************************************************************
"""

import flask

from api_wmiys.common import security
from api_wmiys.common import responses
from api_wmiys.services import search_products as search_products_services
from api_wmiys.domain.enums.product_categories import UrlCategoryNames

# Flask blueprint
bp_search_products = flask.Blueprint('searchProducts', __name__)


#-----------------------------------------------------
# Seach all
# ----------------------------------------------------
@bp_search_products.get('')
@security.login_required
def searchAll():
    return search_products_services.respones_GET_ALL()

#-----------------------------------------------------
# Seach by a specified product category
# ----------------------------------------------------
@bp_search_products.get('categories/<string:category_name>/<int:category_id>')
@security.login_required
@search_products_services.validate_url_category_name
def searchProductCategoriesSub(category_name: str, category_id: int):
    category = UrlCategoryNames(category_name.lower())

    if category == UrlCategoryNames.MAJOR:
        return search_products_services.respones_GET_MAJOR(category_id)     # Seach major categories
    elif category == UrlCategoryNames.MINOR:
        return search_products_services.respones_GET_MINOR(category_id)     # Seach minor categories  
    elif category == UrlCategoryNames.SUB:
        return search_products_services.respones_GET_SUB(category_id)       # Seach sub categories
    else:
        return responses.notFound()

    
    