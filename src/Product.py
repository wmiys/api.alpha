#************************************************************************************
#
#                           Product Class
#
#************************************************************************************

from DB import DB

class Product:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None, user_id=None, name=None, description=None, product_categories_sub_id=None, location_id=None, price_full=None, price_half=None, image=None, created_on=None):
        self.id                        = id
        self.user_id                   = user_id
        self.name                      = name
        self.description               = description
        self.product_categories_sub_id = product_categories_sub_id
        self.location_id               = location_id
        self.price_full                = price_full
        self.price_half                = price_half
        self.image                     = image
        self.created_on                = created_on
    
    #------------------------------------------------------
    # Insert the product into the database
    #------------------------------------------------------
    def insert(self):
        self.id = DB.insertProduct(self.user_id, self.name, self.description, self.product_categories_sub_id, self.location_id, self.price_full, self.price_half, self.image)
    
    #------------------------------------------------------
    # Loads the product data fields from the database
    #------------------------------------------------------
    def loadData(self):
        # make sure the product id is set
        if self.id == None:
            return
        
        db_row = DB.getProduct(self.id)

        self.user_id                   = db_row.user_id
        self.name                      = db_row.name
        self.description               = db_row.description
        self.product_categories_sub_id = db_row.product_categories_sub_id
        self.location_id               = db_row.location_id
        self.price_full                = db_row.price_full
        self.price_half                = db_row.price_half
        self.image                     = db_row.image
        self.created_on                = db_row.created_on



    #------------------------------------------------------
    # Fetch the product data from the database
    #------------------------------------------------------
    def get(self):
        # make sure the product id is set
        if self.id == None:
            return None

        productDbRow = DB.getProduct(self.id)
        return productDbRow
        

        
        








