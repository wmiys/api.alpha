"""
Package:        product_availability
Url Prefix:     /product-categories
Description:    Handles all the product category routing.
"""

import flask
from ..models import product_categories

bp_product_categories = flask.Blueprint('product_categories', __name__)


#------------------------------------------------------
# Returns all categories
#------------------------------------------------------
@bp_product_categories.get('')
def productCatgories():
    seperateFlag = flask.request.args.get('seperate')

    if not seperateFlag:
        return flask.jsonify(product_categories.getAll())

    
    seperateCategories = product_categories.getAllSeperate()
    return flask.jsonify(seperateCategories)


#------------------------------------------------------
# All major categories
#------------------------------------------------------
@bp_product_categories.get('major')
def product_categoriesMajors():
    return flask.jsonify(product_categories.getMajors())


#------------------------------------------------------
# Single major category
#------------------------------------------------------
@bp_product_categories.get('major/<int:major_id>')
def product_categoriesMajor(major_id: int):
    return flask.jsonify(product_categories.getMajor(major_id))


#------------------------------------------------------
# Returns all minor category children of a major product category
#------------------------------------------------------
@bp_product_categories.get('major/<int:major_id>/minor')
def product_categoriesMinors(major_id: int):
    return flask.jsonify(product_categories.getMinors(major_id))


#------------------------------------------------------
# Returns a single minor category
#------------------------------------------------------
@bp_product_categories.get('major/<int:major_id>/minor/<int:minor_id>')
def product_categoriesMinor(major_id: int, minor_id: int):    
    return flask.jsonify(product_categories.getMinor(minor_id))


#------------------------------------------------------
# Returns all sub categories of a minor category
#------------------------------------------------------
@bp_product_categories.get('major/<int:major_id>/minor/<int:minor_id>/sub')
def product_categoriesSubs(major_id: int, minor_id: int):
    return flask.jsonify(product_categories.getSubs(minor_id))


#------------------------------------------------------
# Returns a single sub category
#------------------------------------------------------
@bp_product_categories.get('major/<int:major_id>/minor/<int:minor_id>/sub/<int:sub_id>')
def product_categoriesSub(major_id: int, minor_id: int, sub_id: int):
    return flask.jsonify(product_categories.getSub(sub_id))
