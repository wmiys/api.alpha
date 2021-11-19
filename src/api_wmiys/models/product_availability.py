"""
**********************************************************************************************
A product availability record represents a lender provided date range that they do not wish for
their product to be available for rent. 

So renters will not be able to see the product in the search results if their start/end date range
conflicts with any product availability record.

Furthermore, products that have conflicting availability records will not be able to even receive 
requests from renters if the starts/ends range conflicts.
**********************************************************************************************
"""

from __future__ import annotations
from wmiys_common import utilities
from ..db import DB

class ProductAvailability:

    #------------------------------------------------------
    # Returns all product availability records for a single product
    #
    # Parms:
    #   product_id - the product id
    #
    # Returns: list of product availability records
    #------------------------------------------------------
    @staticmethod
    def getProductAvailabilities(product_id: int) -> list[dict]:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT   *
        FROM     View_Product_Availability pa
        WHERE    pa.product_id = %s
        ORDER BY pa.created_on DESC
        """

        parms = (product_id,)
        cursor.execute(sql, parms)
        availabilities = cursor.fetchall()
        db.close()

        return availabilities
    
    
    #------------------------------------------------------
    # Constructor
    #
    # Parms:
    #   id - product availability id
    #   product_id - product id
    #   starts_on - starts on
    #   ends_on - ends on
    #   note - note 
    #   created_on - created on
    #------------------------------------------------------
    def __init__(self, id=None, product_id=None, starts_on=None, ends_on=None, note=None, created_on=None):
        self.id         = id
        self.product_id = product_id
        self.starts_on  = starts_on
        self.ends_on    = ends_on
        self.note       = note
        self.created_on = created_on


    #------------------------------------------------------
    # Returns the product availability record from the database.
    #
    # This method does NOT set the object properties.
    # It simply returns the record fetched from the database.
    #------------------------------------------------------
    def get(self):
        return self._getDatabaseRecord()

    #------------------------------------------------------
    # Updates the database record to the current object property values.
    #
    # Returns: number of rows affected by the sql statement, or -1 if error
    #------------------------------------------------------
    def update(self) -> int:
        if not self.id:
            return -1

        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        UPDATE Product_Availability
        SET
            product_id = %s,
            starts_on  = %s,
            ends_on    = %s,
            note       = %s
        WHERE 
            id = %s
        """

        parms = (self.product_id, self.starts_on, self.ends_on, self.note, self.id)
        cursor.execute(sql, parms)
        db.commit()
        row_count = cursor.rowcount
        db.close()

        return row_count

    #------------------------------------------------------
    # Delete the product availability record
    #
    # Returns: number of rows affected by the sql statement, or -1 if error
    #------------------------------------------------------
    def delete(self):
        if self.id == None:
            return -1

        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        DELETE FROM Product_Availability
        WHERE id = %s
        """

        parms = (self.id,)
        cursor.execute(sql, parms)
        db.commit()
        row_count = cursor.rowcount
        db.close()

        return row_count
    


    #------------------------------------------------------
    # Insert the product availability into the database
    #
    # Returns: number of rows affected by the sql statement, or -1 if error
    #------------------------------------------------------
    def insert(self):
        if not self.product_id:
            return -1

        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = """
        INSERT INTO Product_Availability 
        (product_id, starts_on, ends_on, note) VALUES
        (%s, %s, %s, %s)
        """

        parms = (self.product_id, self.starts_on, self.ends_on, self.note)

        cursor.execute(sql, parms)
        db.commit()
        row_count = cursor.rowcount
        self.id = cursor.lastrowid
        db.close()

        return row_count

    #------------------------------------------------------
    # Loads the product data fields from the database
    #------------------------------------------------------
    def loadData(self):
        availability_record = self._getDatabaseRecord()
        self.setPropertyValuesFromDict(availability_record)


    #------------------------------------------------------
    # Retrieve the product availability record from the database
    #------------------------------------------------------
    def _getDatabaseRecord(self) -> dict:
        # make sure the product id is set
        if self.id == None:
            return None

        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT      *
        FROM        View_Product_Availability pa
        WHERE       pa.id = %s
        ORDER BY    pa.created_on DESC
        LIMIT       1
        """

        parms = (self.id,)

        cursor.execute(sql, parms)
        product_availability_record = cursor.fetchone()
        db.close()

        return product_availability_record

    #------------------------------------------------------
    # Set's the object's properties given a dict
    #
    # Parms:
    #   newPropertyValues - a dict containing all of the objects properties
    #
    # Returns: bool
    #   true - properties were successfully changed
    #   false - the dict contained an extraneous field.
    #------------------------------------------------------
    def setPropertyValuesFromDict(self, newPropertyValues: dict):
        # validate the field before changing the object property
        if not utilities.areAllKeysValidProperties(newPropertyValues, self):
            return False

        # set the object properties
        for key in newPropertyValues:
            if newPropertyValues[key]:
                setattr(self, key, newPropertyValues[key])
            else:
                setattr(self, key, None)
            
        return True


