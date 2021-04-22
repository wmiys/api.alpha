#************************************************************************************
#
#                           Product Availability Model
#
#************************************************************************************

from DB import DB


class ProductAvailability:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None, product_id=None, starts_on=None, ends_on=None, note=None, created_on=None):
        self.id         = id
        self.product_id = product_id
        self.starts_on  = starts_on
        self.ends_on    = ends_on
        self.note       = note
        self.created_on = created_on


    @staticmethod
    def getProductAvailabilities(product_id: int):
        return DB.getProductAvailabilities(product_id)
    



