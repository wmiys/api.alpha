#************************************************************************************
#
#                           Product Availability Model
#
#************************************************************************************

from DB import DB


class ProductAvailability:
    """Product Availability Model
    """

    @staticmethod
    def getProductAvailabilities(product_id: int) -> list:
        """Returns all product availability records for a single product

        Args:
            product_id (int): the product id

        Returns:
            list: all the product availability records in the database
        """
        return DB.getProductAvailabilities(product_id)
    
    
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


    def get(self):
        """Returns the product availability record from the database
        """
        # make sure the product id is set
        if self.id == None:
            return None

        dbRow = DB.getProductAvailability(self.id)
        return dbRow
        

        



