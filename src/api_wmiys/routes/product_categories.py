"""
Package:        product_availability
Url Prefix:     /product-categories
Description:    Handles all the product category routing.
"""

import os
from flask import Blueprint, jsonify, request
from ..models import ProductCategories

product_categories = Blueprint('product_categories', __name__)

@product_categories.route('', methods=['GET'])
def productCatgories():
    """Returns all categories
    """

    seperateFlag = request.args.get('seperate')

    if not seperateFlag:
        return jsonify(ProductCategories.getAll())

    
    seperateCategories = ProductCategories.getAllSeperate()
    return jsonify(seperateCategories)


@product_categories.route('major', methods=['GET'])
def productCategoriesMajors():
    """Returns all major categories
    """
    return jsonify(ProductCategories.getMajors())


@product_categories.route('major/<int:major_id>', methods=['GET'])
def productCategoriesMajor(major_id: int):
    """Returns a single major category

    Args:
        major_id (int): major category id
    """
    return jsonify(ProductCategories.getMajor(major_id))

@product_categories.route('major/<int:major_id>/minor', methods=['GET'])
def productCategoriesMinors(major_id: int):
    """Returns all minor category children of a major product category

    Args:
        major_id (int): major category id
    """
    return jsonify(ProductCategories.getMinors(major_id))


@product_categories.route('major/<int:major_id>/minor/<int:minor_id>', methods=['GET'])
def productCategoriesMinor(major_id: int, minor_id: int):
    """Returns a single minor category

    Args:
        major_id (int): major product category id
        minor_id (int): minor product category id
    """
    
    return jsonify(ProductCategories.getMinor(minor_id))


@product_categories.route('major/<int:major_id>/minor/<int:minor_id>/sub', methods=['GET'])
def productCategoriesSubs(major_id: int, minor_id: int):
    """Returns all sub categories of a minor category

    Args:
        major_id (int): major product category id
        minor_id (int): minor product category id
    """
    return jsonify(ProductCategories.getSubs(minor_id))


@product_categories.route('major/<int:major_id>/minor/<int:minor_id>/sub/<int:sub_id>', methods=['GET'])
def productCategoriesSub(major_id: int, minor_id: int, sub_id: int):
    """Returns a single sub category

    Args:
        major_id (int): major product category id
        minor_id (int): minor product category id
        sub_id (int): sub product category id
    """
    return jsonify(ProductCategories.getSub(sub_id))
