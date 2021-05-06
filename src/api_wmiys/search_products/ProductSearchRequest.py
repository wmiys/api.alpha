#************************************************************************************
#
#                           Product Search Request
#
#************************************************************************************
import datetime
import typing
from api_wmiys.DB.DB import DB
from enum import Enum
import collections



class ProductSearchRequest:
    """The product search request is responsible for handling all of the product search requests.
    """

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

    def searchAll(self):
        """Search for a major product category

        Args:
            product_categories_major_id (int): id of the major product category

        Returns:
            list: matching products
        """
        
        return DB.searchProductsAll(self.location_id, self.starts_on, self.ends_on)

    def searchCategoriesMajor(self, product_categories_major_id: int):
        """Search for a major product category

        Args:
            product_categories_major_id (int): id of the major product category

        Returns:
            list: matching products
        """

        return self.searchCategoriesBase(1, product_categories_major_id)


    def searchCategoriesMinor(self, product_categories_minor_id: int):
        """Search for a minor product category

        Args:
            product_categories_minor_id (int): id of the minor product category

        Returns:
            list: matching products
        """

        return self.searchCategoriesBase(2, product_categories_minor_id)
        

    def searchCategoriesSub(self, product_categories_sub_id: int):
        """Search for a sub product category

        Args:
            product_categories_sub_id (int): id of the sub product category

        Returns:
            list: matching products
        """

        return self.searchCategoriesBase(3, product_categories_sub_id)


    def searchCategoriesBase(self, product_category_type, product_category_id):
        """Base function for searchProducts[Major,Minor,Sub] to call

        product_category_type needs to be either 1, 2, or 3:

            1 = major categories
            2 = minor categories
            3 = sub categories


        Args:
            product_category_type (int): type of product category to search for
            product_category_id (int): the id of the product category

        Returns:
            list: the results of the search query
        """
        results = DB.searchProductsByCategory(self.location_id, self.starts_on, self.ends_on, product_category_type, product_category_id)

        return results




