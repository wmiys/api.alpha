#----------------------------------------------------------------------------------- 
#
# This class handles all the product-category requests
#
#-----------------------------------------------------------------------------------

from DB import DB

class ProductCategories:

    @staticmethod
    def getMajors():
        return DB.getProductCategoryMajors()
    

    @staticmethod
    def getMajor(id: int):
        return DB.getProductCategoryMajor(id)
    
    @staticmethod
    def getMinors(parent_id: int):
        return DB.getProductMajorCategoryChildren(parent_id)
    
    @staticmethod
    def getMinor(id: int):
        return DB.getProductCategoryMinor(id)
    
    @staticmethod
    def getSubs(parent_id: int):
        return DB.getProductMinorCategoryChildren(parent_id)
    
    @staticmethod
    def getSub(id: int):
        return DB.getProductCategorySub(id)
    
    
