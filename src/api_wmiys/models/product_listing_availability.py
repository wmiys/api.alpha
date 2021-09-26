from ..db import DB

class ProductListingAvailability:

    def __init__(self, product_id: int=None, location_id: int=None, starts_on: str=None, ends_on: str=None):
        self.product_id = product_id
        self.location_id = location_id
        self.starts_on = starts_on
        self.ends_on = ends_on

    
    def areAllPropertiesSet(self) -> bool:
        """Checks if all the object fields are set (or not null)

        Returns:
            bool: true - no fields have None value, false - one of them has a null value
        """
        if None in [self.product_id, self.location_id, self.starts_on, self.ends_on]:
            return False
        else:
            return True


    def isProductAvailable(self) -> bool:
        """Checks if the product is available during the dates and location

        Returns:
            bool: true - product is available, false - product is not available
        """
        if not self.areAllPropertiesSet():
            return False
        
        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = 'SELECT SEARCH_PRODUCTS_FILTER(%s, %s, %s, %s) AS result'

        parms = (self.product_id, self.location_id, self.starts_on, self.ends_on)
        mycursor.execute(sql, parms)
        dbResult = mycursor.fetchone()

        DB.mydb.close()

        if dbResult.result == 0:
            return False
        else:
            return True






