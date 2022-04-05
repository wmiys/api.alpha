"""
**********************************************************************************************
This class handles all the product-category requests.
All products must be assigned a specific sub-category id.
**********************************************************************************************
"""

from __future__ import annotations

from api_wmiys.repository import product_categories as repo

#------------------------------------------------------
# Returns all categories
#------------------------------------------------------
def getAll() -> dict:
    return _getProductCategories()


#------------------------------------------------------
# Fetch all the product category records, and split them up into different levels
#------------------------------------------------------
def getAllSeperate() -> dict:
    category_record_table = _getProductCategories()

    majors = []
    minors = []
    subs = []

    for category in category_record_table:
        major = dict(id=category.get('major_id'), name=category.get('major_name'))
        minor = dict(id=category.get('minor_id'), name=category.get('minor_name'), parent_id=category.get('major_id'))
        sub = dict(id=category.get('sub_id'), name=category.get('sub_name'), parent_id=category.get('minor_id'))
        
        if major not in majors:
            majors.append(major)
        if minor not in minors:
            minors.append(minor)
        if sub not in subs:
            subs.append(sub)

    return dict(major=majors, minor=minors, sub=subs)

#------------------------------------------------------
# Get all the product categories
#------------------------------------------------------
def _getProductCategories() -> list[dict]:
    return repo.selectAll()

#------------------------------------------------------
# Retrieve all major categories
#------------------------------------------------------
def getMajors() -> list[dict]:
    return repo.selectMajors().data

#------------------------------------------------------
# Retrieve a single major category
#------------------------------------------------------
def getMajor(major_category_id: int) -> dict:
    return repo.selectMajor(major_category_id).data

#------------------------------------------------------
# Retrieve all minor categories belonging to a major category
#------------------------------------------------------
def getMinors(parent_category_id: int) -> list[dict]:
    return repo.selectMinors(parent_category_id).data

#------------------------------------------------------
# Retrieve a single minor category
#------------------------------------------------------
def getMinor(minor_category_id: int) -> dict:
    return repo.selectMinor(minor_category_id).data

#------------------------------------------------------
# Retrieve all sub categories beloning to a minor category
#------------------------------------------------------
def getSubs(parent_category_id: int) -> list[dict]:
    return repo.selectSubs(parent_category_id).data

#------------------------------------------------------
# Retrieve a single sub category
#------------------------------------------------------
def getSub(sub_category_id: int) -> dict:
    return repo.selectSub(sub_category_id).data


