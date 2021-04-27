from flask import Blueprint, jsonify
from api_wmiys.product_categories.Product_Categories import ProductCategories
import os

product_categories = Blueprint('product_categories', __name__)


#------------------------------------------------------
# All categories
#------------------------------------------------------
@product_categories.route('', methods=['GET'])
def productCatgories():
    return jsonify(ProductCategories.getAll())

#------------------------------------------------------
# all major categories
#------------------------------------------------------
@product_categories.route('major', methods=['GET'])
def productCategoriesMajors():
    return jsonify(ProductCategories.getMajors())

#------------------------------------------------------
# single major category
#------------------------------------------------------
@product_categories.route('major/<int:major_id>', methods=['GET'])
def productCategoriesMajor(major_id):
    return jsonify(ProductCategories.getMajor(major_id))

#------------------------------------------------------
# all minor categories of a major
#------------------------------------------------------
@product_categories.route('major/<int:major_id>/minor', methods=['GET'])
def productCategoriesMinors(major_id):
    return jsonify(ProductCategories.getMinors(major_id))

#------------------------------------------------------
# single minor category
#------------------------------------------------------
@product_categories.route('major/<int:major_id>/minor/<int:minor_id>', methods=['GET'])
def productCategoriesMinor(major_id, minor_id):
    return jsonify(ProductCategories.getMinor(minor_id))

#------------------------------------------------------
# all sub categories of a minor
#------------------------------------------------------
@product_categories.route('major/<int:major_id>/minor/<int:minor_id>/sub', methods=['GET'])
def productCategoriesSubs(major_id, minor_id):
    return jsonify(ProductCategories.getSubs(minor_id))

#------------------------------------------------------
# single sub category
#------------------------------------------------------
@product_categories.route('major/<int:major_id>/minor/<int:minor_id>/sub/<int:sub_id>', methods=['GET'])
def productCategoriesSub(major_id, minor_id, sub_id):
    return jsonify(ProductCategories.getSub(sub_id))

