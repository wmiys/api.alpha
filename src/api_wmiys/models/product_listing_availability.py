from ..db import DB

class ProductListingAvailability:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, product_id: int=None, location_id: int=None, starts_on: str=None, ends_on: str=None):
        self.product_id = product_id
        self.location_id = location_id
        self.starts_on = starts_on
        self.ends_on = ends_on


    #------------------------------------------------------
    # Checks if all the object fields are set (or not null)
    #
    # Returns a bool:
    #   true - no fields have None value
    #   false - one of them has a null value
    #------------------------------------------------------    
    def areAllPropertiesSet(self) -> bool:
        if None in [self.product_id, self.location_id, self.starts_on, self.ends_on]:
            return False
        else:
            return True

    #------------------------------------------------------
    # hecks if the product is available during the dates and location
    #
    # Returns a bool:
    #   true - product is available
    #   false - product is not available
    #------------------------------------------------------ 
    def isProductAvailable(self) -> bool:
        if not self.areAllPropertiesSet():
            return False
        
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = 'SELECT SEARCH_PRODUCTS_FILTER(%s, %s, %s, %s) AS result'
        parms = (self.product_id, self.location_id, self.starts_on, self.ends_on)
        cursor.execute(sql, parms)
        record_set = cursor.fetchone()

        db.close()

        if record_set.get('result') == 0:
            return False
        else:
            return True






