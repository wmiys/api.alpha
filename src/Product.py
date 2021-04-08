#************************************************************************************
#
#                           Product Class
#
#************************************************************************************

from DB import DB
from Utilities import Utilities
from typing import Optional

class Product:

    
    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None, user_id=None, name=None, description=None, product_categories_sub_id=None, location_id=None, dropoff_distance=None, price_full=None, price_half=None, image=None, minimum_age=None, created_on=None):
        self.id                        = id
        self.user_id                   = user_id
        self.name                      = name
        self.description               = description
        self.product_categories_sub_id = product_categories_sub_id
        self.location_id               = location_id
        self.dropoff_distance          = dropoff_distance
        self.price_full                = price_full
        self.price_half                = price_half
        self.image                     = image
        self.minimum_age               = minimum_age
        self.created_on                = created_on
    
    #------------------------------------------------------
    # Insert the product into the database
    #------------------------------------------------------
    def insert(self):
        self.id = DB.insertProduct(self.user_id, self.name, self.description, self.product_categories_sub_id, self.location_id, self.dropoff_distance, self.price_full, self.price_half, self.image, self.minimum_age)
    
    #------------------------------------------------------
    # Update the product database record
    #------------------------------------------------------
    def update(self):
        dbResult = DB.updateProduct(product_id=self.id, name=self.name, description=self.description, 
                                    product_categories_sub_id=self.product_categories_sub_id,
                                    location_id=self.location_id, dropoff_distance=self.dropoff_distance, 
                                    price_full=self.price_full, price_half=self.price_half, image=self.image, 
                                    minimum_age=self.minimum_age)
        
        return dbResult.rowcount

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
        self.dropoff_distance          = db_row.dropoff_distance
        self.price_full                = db_row.price_full
        self.price_half                = db_row.price_half
        self.image                     = db_row.image
        self.minimum_age               = db_row.minimum_age
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
    
    #------------------------------------------------------
    # Set's the object's properties given a dict
    #
    # Returns boolean:
    #   false: the dict contained an extraneous field
    #   true: properties were successfully changed
    #------------------------------------------------------
    def setPropertyValuesFromDict(self, newPropertyValues: dict):
        # validate the field before changing the object property
        if not Utilities.areAllKeysValidProperties(newPropertyValues, self):
            return False

        # set the object properties
        for key in newPropertyValues:
            if newPropertyValues[key]:
                setattr(self, key, newPropertyValues[key])
            else:
                setattr(self, key, None)
            
        return True




            

        
        








