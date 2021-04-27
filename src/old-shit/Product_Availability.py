#************************************************************************************
#
#                           Product Availability Model
#
#************************************************************************************

from DB import DB
from Utilities import Utilities


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
        """Returns the product availability record from the database.

        Note: This method does NOT set the object properties. It simply returns the record fetched from the database.
        """
        # make sure the product id is set
        if self.id == None:
            return None

        dbRow = DB.getProductAvailability(self.id)
        return dbRow
    
    def loadData(self):
        """Loads the product data fields from the database
        """
        # ensure the id is set
        if self.id == None:
            return
        
        dbResult = DB.getProductAvailability(self.id)
        self.setPropertyValuesFromDict(dbResult._asdict())


    def update(self):
        """Updates the database record to the current object property values
        """
        dbResult = DB.updateProductAvailability(id=self.id, product_id=self.product_id, starts_on=self.starts_on, ends_on=self.ends_on, note=self.note)
        return dbResult

    def setPropertyValuesFromDict(self, newPropertyValues: dict):
        """Set's the object's properties given a dict

        Args:
            newPropertyValues (dict): a dict containing all of the objects properties

        Returns:
            bool: 
                false: the dict contained an extraneous field.
                true: properties were successfully changed
        """
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
    
    def delete(self):
        """Delete the product availability

        Returns:
            mysql cursor: returns the database cursor used
        """

        if self.id == None:
            return

        dbResult = DB.deleteProductAvailability(self.id)
        return dbResult
    
    def insert(self):
        """Insert the product availability into the database
        """
        newProductAvailabilityID = DB.insertProductAvailability(self.product_id, self.starts_on, self.ends_on, self.note)
        self.id = newProductAvailabilityID

        



