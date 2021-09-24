from api_wmiys.DB.DB import DB
from .product import Product

class ProductListing:

    def __init__(self, product_id: int=None):
        self.product_id = product_id
        self._dbResult = None

    @property
    def dbResult(self) -> object:
        if not self._dbResult:
            self.load()
        
        return self._dbResult


    
    def get(self) -> dict:
        """Retrieve the product listing data as a dictionary object

        ---
        The dict returned represents a json object with these fileds:

        - meta
        - price
        - categories
        - lender


        Returns:
            dict: product listing dictionary.
        """

        metaDict = self.getMetaDict()
        priceDict = self.getPriceDict()
        categoriesDict = self.getCategoriesDict()        
        lenderDict = self.getLenderDict()

        outputDict = dict(meta=metaDict, price=priceDict, categories=categoriesDict, lender=lenderDict)

        

        return outputDict
        

    def load(self) -> None:
        """Load the data from the database.
        """        

        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT * FROM View_Product_Listings vpl
        WHERE vpl.id = %s
        """

        parms = (self.product_id,)
        mycursor.execute(sql, parms)
        self._dbResult = mycursor.fetchone()

        DB.mydb.close()


    def getMetaDict(self) -> dict:
        """Get the meta json object.

        ---
        Returns a dict containing these fields:

        - description
        - id
        - image
        - minimum_age
        - name

        ---
        Returns:
            dict: meta object
        """

        img = Product.LOCAL_SERVER_COVER_PHOTO_DIRECTORY_ABS + '/' + self.dbResult.image
        metaDict = dict(id=self.dbResult.id, name=self.dbResult.name, description=self.dbResult.description, minimum_age=self.dbResult.minimum_age, image=img)
        return metaDict
    
    def getPriceDict(self) -> dict:
        """Get the price json object.

        ---
        Returns a dict containing these fields:

        - full
        - half

        ---
        Returns:
            dict: meta object
        """

        priceDict = dict(full=self.dbResult.price_full, half=self.dbResult.price_half)
        return priceDict

    
    def getCategoriesDict(self) -> dict:
        """Get the categories json object.
        
        ---
        Returns a dict containing these fields:

        - major_id
        - major_name
        - minor_id
        - minor_name
        - sub_id
        - sub_name

        ---
        Returns:
            dict: meta object
        """
        categoriesDict = dict(major_id=self.dbResult.product_categories_major_id, major_name=self.dbResult.product_categories_major_name, 
            minor_id=self.dbResult.product_categories_minor_id, minor_name=self.dbResult.product_categories_minor_name, 
            sub_id=self.dbResult.product_categories_sub_id, sub_name=self.dbResult.product_categories_sub_name)

        return categoriesDict

    def getLenderDict(self) -> dict:
        """Get the lender json object.

        ---
        Returns a dict containing these fields:

        - id
        - name_first
        - name_last

        ---
        Returns:
            dict: meta object
        """

        lenderDict = dict(id=self.dbResult.lender_id, name_first=self.dbResult.lender_name_first, name_last=self.dbResult.lender_name_last)
        return lenderDict
    



    
