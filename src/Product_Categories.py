#************************************************************************************
#
# This class handles all the product-category requests.
#
#************************************************************************************

from DB import DB
from collections import namedtuple

class ProductCategories:

    #------------------------------------------------------
    # Returns all categories
    #------------------------------------------------------
    @staticmethod
    def getAll():
        categories = DB.getProductCategories()

        majors = []
        minors = []
        subs = []


        # break down table into major, minor, and sub categories
        for category in categories:
            major = dict(id=category.major_id, name=category.major_name, minor=[])

            if major not in majors:     # no duplicates
                majors.append(major)
            
            minor = dict(id=category.minor_id, name=category.minor_name, product_categories_major_id=category.major_id, sub=[])

            if minor not in minors:     # no duplicates
                minors.append(minor)

            sub = dict(id=category.sub_id, name=category.sub_name, product_categories_minor_id=category.minor_id)

            if sub not in subs:         # no duplicates
                subs.append(sub)

        # put all sub categories into their parent lists
        for sub in subs:
            for minor in minors:

                if minor['id'] == sub['product_categories_minor_id']:
                    minor['sub'].append(sub)

        # put all minor categories into their parent lists
        for minor in minors:
            for major in majors:

                if major['id'] == minor['product_categories_major_id']:
                    major['minor'].append(minor)
        
        return majors

    #------------------------------------------------------
    # Retrieve all major categories
    #------------------------------------------------------
    @staticmethod
    def getMajors():
        return DB.getProductCategoryMajors()
    
    #------------------------------------------------------
    # Retrieve a single major category
    #------------------------------------------------------
    @staticmethod
    def getMajor(id: int):
        return DB.getProductCategoryMajor(id)
    
    #------------------------------------------------------
    # Retrieve all minor categories beloning to a major category
    #------------------------------------------------------
    @staticmethod
    def getMinors(parent_id: int):
        return DB.getProductMajorCategoryChildren(parent_id)
    
    #------------------------------------------------------
    # Retrieve a single minor category
    #------------------------------------------------------
    @staticmethod
    def getMinor(id: int):
        return DB.getProductCategoryMinor(id)
    
    #------------------------------------------------------
    # Retrieve all sub categories beloning to a minor category
    #------------------------------------------------------
    @staticmethod
    def getSubs(parent_id: int):
        return DB.getProductMinorCategoryChildren(parent_id)
    
    #------------------------------------------------------
    # Retrieve a single sub category
    #------------------------------------------------------
    @staticmethod
    def getSub(id: int):
        return DB.getProductCategorySub(id)
    
    
