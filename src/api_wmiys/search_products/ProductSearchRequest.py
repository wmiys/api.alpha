import datetime
import typing
from api_wmiys.DB.DB import DB


class ProductSearchRequest:

    def __init__(self, location_id=None, starts_on=None, ends_on=None):
        """Constructor for ProductSearchRequest

        Args:
            location_id (int): location id of the dropoff point
            starts_on (datetime): when the renter would like to start renting the product
            ends_on (datetime): when the renter is done renting the product
        """
        self.location_id = location_id
        self.starts_on = starts_on
        self.ends_on = ends_on
    
    def areRequiredPropertiesSet(self) -> bool:
        """Checks if the required object properties are set 
        
        The required properties are::

            location_id
            starts_on
            ends_on

        Returns:
            bool: true if location_id, starts_on, and ends_on are set. Otherwise returns false.
        """ 
        if not self.location_id:
            return False
        elif not self.starts_on:
            return False
        elif not self.ends_on:
            return False
        else:
            return True


    def searchCategoriesSub(self, product_categories_sub_id: int):
        """Search for a sub product category

        Args:
            product_categories_sub_id (int): id of the sub product category

        Returns:
            list: matching products
        """
        return DB.searchProductsCategorySub(self.location_id, self.starts_on, self.ends_on, product_categories_sub_id)






