"""
**********************************************************************************************
A product listing represents a product that is publicly visible to all renters. This is what
data is used when a renter goes to a product-listing page. 

It's essentially the same thing as the product view from the lender's side.

I just thought it would be a good idea to seperate out the views for security... might have been a mistake.
**********************************************************************************************
"""

from ..db import DB
from ..common import user_image

class ProductListing:

    #----------------------------------------------------------
    # Constructor
    #----------------------------------------------------------
    def __init__(self, product_id: int=None):
        self.product_id = product_id
        self._dbResult = None

    @property
    def dbResult(self) -> object:
        if not self._dbResult:
            self.load()
        
        return self._dbResult


    #----------------------------------------------------------
    # Retrieve the product listing data as a dictionary object
    #
    # The dict returned represents a json object with these fileds:
    #   - meta
    #   - price
    #   - categories
    #   - lender
    #
    # Returns:
    #     dict: product listing dictionary.
    #----------------------------------------------------------
    def get(self) -> dict:
        product_listing = dict(
            meta       = self._getMetaDict(),
            price      = self._getPriceDict(),
            categories = self._getCategoriesDict(),
            lender     = self._getLenderDict()
        )

        return product_listing

        
    #----------------------------------------------------------
    # Load the data from the database.
    #----------------------------------------------------------
    def load(self) -> None:
        db = DB()
        db.connect()
        mycursor = db.getCursor(True)

        sql = """
        SELECT * FROM View_Product_Listings vpl
        WHERE vpl.id = %s
        """

        parms = (self.product_id,)
        mycursor.execute(sql, parms)
        self._dbResult = mycursor.fetchone()

        db.close()

    #----------------------------------------------------------
    # Get the meta json object.
    #
    # Returns a dict containing these fields:
    #   - description
    #   - id
    #   - image
    #   - minimum_age
    #   - name
    #
    # Returns:
    #     dict: meta object
    #----------------------------------------------------------
    def _getMetaDict(self) -> dict:

        if self.dbResult.get('image'):
            prefix = user_image.getCoverUrl()
            img = prefix + self.dbResult.get('image')
        else:
            img = None

        metaDict = dict(
            id          = self.dbResult.get('id'),
            name        = self.dbResult.get('name'),
            description = self.dbResult.get('description'),
            minimum_age = self.dbResult.get('minimum_age'),
            image       = img
        )

        return metaDict
    

    #----------------------------------------------------------
    # Get the price json object.
    #
    # Returns a dict containing these fields:
    #   - full
    #   - half
    #
    # Returns:
    #     dict: meta object
    #----------------------------------------------------------
    def _getPriceDict(self) -> dict:

        priceDict = dict(
            full = self.dbResult.get('price_full'),
        )

        return priceDict

    #----------------------------------------------------------
    # Get the categories json object.
    #
    # Returns a dict containing these fields:
    #   - major_id
    #   - major_name
    #   - minor_id
    #   - minor_name
    #   - sub_id
    #   - sub_name
    #
    # Returns:
    #     dict: meta object
    #----------------------------------------------------------
    def _getCategoriesDict(self) -> dict:
        categoriesDict = dict(
            major_id   = self.dbResult.get('product_categories_major_id'),
            major_name = self.dbResult.get('product_categories_major_name'),
            minor_id   = self.dbResult.get('product_categories_minor_id'),
            minor_name = self.dbResult.get('product_categories_minor_name'),
            sub_id     = self.dbResult.get('product_categories_sub_id'),
            sub_name   = self.dbResult.get('product_categories_sub_name'),
        )

        return categoriesDict

    #----------------------------------------------------------
    # Get the lender json object.
    #
    # Returns a dict containing these fields:
    #   - id
    #   - name_first
    #   - name_last
    #
    # Returns:
    #     dict: meta object
    #----------------------------------------------------------
    def _getLenderDict(self) -> dict:        
        lenderDict = dict(
            id         = self.dbResult.get('lender_id'),
            name_first = self.dbResult.get('lender_name_first'),
            name_last  = self.dbResult.get('lender_name_last'),
        )

        return lenderDict
    



    
