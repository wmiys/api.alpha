#************************************************************************************
#
# This class handles all the product-category requests.
#
#************************************************************************************

from api_wmiys.DB.DB import DB
from collections import namedtuple

class ProductCategories:

    #------------------------------------------------------
    # Returns all categories
    #------------------------------------------------------
    @staticmethod
    def getAll():
        categories = DB.getProductCategories()
        return categories

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
    
    
