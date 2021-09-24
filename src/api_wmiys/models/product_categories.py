#************************************************************************************
#
# This class handles all the product-category requests.
#
#************************************************************************************

from ..db import DB
from collections import namedtuple

class ProductCategories:

    #------------------------------------------------------
    # Returns all categories
    #------------------------------------------------------
    @staticmethod
    def getAll():
        categoryTable = DB.getProductCategories()
        return categoryTable

    @staticmethod
    def getAllSeperate():
        categoryTable = DB.getProductCategories()

        majors = []
        minors = []
        subs = []

        Major = namedtuple('Major', ['id', 'name'])
        Minor = namedtuple('Minor', ['id', 'name', 'parent_id'])
        Sub   = namedtuple('Sub', ['id', 'name', 'parent_id'])

        for row in categoryTable:
            major = dict(id=row.major_id, name=row.major_name)
            minor = dict(id=row.minor_id, name=row.minor_name, parent_id=row.major_id)
            sub = dict(id=row.sub_id, name=row.sub_name, parent_id=row.minor_id)
            
            if major not in majors:
                majors.append(major)
            if minor not in minors:
                minors.append(minor)
            if sub not in subs:
                subs.append(sub)


        return dict(major=majors, minor=minors, sub=subs)
        

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
    
    
