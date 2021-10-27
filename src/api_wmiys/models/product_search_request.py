#************************************************************************************
#
#                           Product Search Request
#
#************************************************************************************
from __future__ import annotations
import flask
from ..db import DB
from ..common import sorting, Pagination, user_image
from ..models import product
from enum import Enum 


_SQL_STMT_PREFIX = '''
    SELECT * FROM View_Search_Products p
    WHERE SEARCH_PRODUCTS_FILTER(p.id, %s, %s, %s) = TRUE 
'''

# Product category sql table names
PRODUCT_CATEGORY_TABLE_NAME_MAJOR = 'product_categories_major_id'
PRODUCT_CATEGORY_TABLE_NAME_MINOR = 'product_categories_minor_id'
PRODUCT_CATEGORY_TABLE_NAME_SUB   = 'product_categories_sub_id'

    
#----------------------------------------------------------
# Possible filter product categories
#----------------------------------------------------------
class FilterCategories(Enum):
    MAJOR = 1
    MINOR = 2
    SUB   = 3


#----------------------------------------------------------
# The product search request is responsible for handling all of the product search requests.
#----------------------------------------------------------
class ProductSearchRequest:

    #----------------------------------------------------------
    # Constructor
    #
    # Parms:
    #   location_id: location id
    #   starts_on: starts on
    #   ends_on: ends on
    #   sorting: sorting object
    #   oPaginpaginationation: pagination object
    #----------------------------------------------------------
    def __init__(self, location_id=None, starts_on=None, ends_on=None, sorting: sorting.SortingSearchProducts=None, pagination: Pagination=None):
        self.location_id = location_id
        self.starts_on   = starts_on
        self.ends_on     = ends_on
        self.sorting     = sorting
        self.pagination  = pagination
    
    #----------------------------------------------------------
    # Checks if the required object properties are set 
    #
    # The required properties are:
    #   - location_id
    #   - starts_on
    #   - ends_on
    #
    # Returns a bool:
    #   true if location_id, starts_on, and ends_on are set. 
    #   otherwise, false
    #----------------------------------------------------------
    def areRequiredPropertiesSet(self) -> bool:
        if None in [self.location_id, self.starts_on, self.ends_on]:
            return False
        else:
            return True

    #----------------------------------------------------------
    # Search for a all products 
    #
    # Returns a tuple: (records, count)
    #----------------------------------------------------------
    def searchAll(self) -> tuple:
        stmt_template = f'{_SQL_STMT_PREFIX} ORDER BY {self.sorting.field} {self.sorting.type}'
        parms = (self.location_id, self.starts_on, self.ends_on)

        search_result_records, record_count  = self._getSearchRecordsAndCountTuple(stmt_template, parms)

        image_url_prefix = user_image.getCoverUrl()

        for product_result in search_result_records:
            if product_result['image']:
                product_result['image'] = image_url_prefix + product_result['image']

        return (search_result_records, record_count)

    #----------------------------------------------------------
    # Search for products and filter by the given category
    #
    # product_category_type needs to be either 1, 2, or 3:
    #   1 = major categories
    #   2 = minor categories
    #   3 = sub categories
    #
    # Parms:
    #   product_category_type (int): type of product category to search for
    #   product_category_id (int): the id of the product category
    #
    # Returns a list: 
    #   the results of the search query
    #----------------------------------------------------------
    def searchCategories(self, filter_category: FilterCategories, product_category_id: int) -> tuple:
        # create the sql statements
        categoryTableName = self._getSearchProductCategoryTableName(filter_category)

        stmt_template = f'{_SQL_STMT_PREFIX} AND {categoryTableName} = %s ORDER BY {self.sorting.field} {self.sorting.type}'

        # setup the parms
        parms = (self.location_id, self.starts_on, self.ends_on, product_category_id)

        search_result_records, record_count  = self._getSearchRecordsAndCountTuple(stmt_template, parms)

        # img_path_prefix = f'{flask.request.root_url}static/{product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY}/'
        img_path_prefix = user_image.getCoverUrl()

        for product_result in search_result_records:
            if product_result['image']:
                product_result['image'] = img_path_prefix + product_result['image']

        return (search_result_records, record_count)

    #----------------------------------------------------------
    # Helper function that executes the given sql statement with the given parms.
    #----------------------------------------------------------
    def _getSearchRecordsAndCountTuple(self, sql_stmt_prefix, parms) -> tuple:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)
        
        # create the sql statement for fetching the records
        stmtWithLimit = self.pagination.getSqlStmtLimitOffset(sql_stmt_prefix)
        
        # create the sql statement to calculate the count
        stmtTotalCount = self.pagination.getSqlStmtTotalCount(sql_stmt_prefix)

        try:
            # fetch the records
            cursor.execute(stmtWithLimit, parms)
            search_result_records = cursor.fetchall()

            # fetch the count
            cursor.execute(stmtTotalCount, parms)

            record_count = cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            db.close()

        return (search_result_records, record_count.get('count'))


    #----------------------------------------------------------
    # Get the product category table name based on the input
    #
    #     1 = major categories
    #     2 = minor categories
    #     3 = sub categories
    #
    # Args:
    #     a_iProductCategoryType (int): id of the product category table
    #
    # Returns:
    #     str: name of the product category table 
    #----------------------------------------------------------
    def _getSearchProductCategoryTableName(self, category_type: FilterCategories) -> str:
        if category_type == FilterCategories.MAJOR:
            categoryTableName = PRODUCT_CATEGORY_TABLE_NAME_MAJOR
        elif category_type == FilterCategories.MINOR:
            categoryTableName = PRODUCT_CATEGORY_TABLE_NAME_MINOR
        elif category_type == FilterCategories.SUB:
            categoryTableName = PRODUCT_CATEGORY_TABLE_NAME_SUB

        return categoryTableName







