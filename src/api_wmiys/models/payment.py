"""
This class represents a payment record in the database.

payment_session_id represents the session_id generated from the stripe API.
"""

from ..db import DB

class Payment:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None, product_id=None, renter_id=None, dropoff_location_id=None, starts_on=None, ends_on=None, price_full=None, payment_session_id=None, created_on=None):
        self.id                  = id
        self.product_id          = product_id
        self.renter_id           = renter_id
        self.dropoff_location_id = dropoff_location_id
        self.starts_on           = starts_on
        self.ends_on             = ends_on
        self.price_full          = price_full
        self.payment_session_id  = payment_session_id
        self.created_on          = created_on


    #------------------------------------------------------
    # Checks if all the object's required fields to do an
    # insert statement have a value.
    #
    # Returns a bool:
    #   true - all required keys have a value
    #   false - 1 or more required keys do NOT have a value.
    #------------------------------------------------------
    def areAllValidInsertFieldsSet(self) -> bool:
        if None in [self.id, self.product_id, self.renter_id, self.dropoff_location_id, self.starts_on, self.ends_on, self.price_full]:
            return False
        else:
            return True


    #------------------------------------------------------
    # Insert the object into the database
    #------------------------------------------------------
    def insert(self) -> bool:        
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = '''
            INSERT INTO Payments (
                id,                     product_id,         renter_id,
                dropoff_location_id,    starts_on,          ends_on,
                payment_session_id,     price_full
            ) 

            SELECT 
                %s, %s, %s,
                %s, %s, %s,
                %s, p.price_full
            FROM Products p
            WHERE p.id = %s
            LIMIT 1
        '''

        success = False

        try:
            cursor.execute(sql, self._getInsertParms())
            db.commit()
            success = True
        except Exception as e:
            success = False
            print(e)
        finally:
            db.close()
        
        return success
        

    #------------------------------------------------------
    # Returns the tuple required for the insert function parms value.
    #------------------------------------------------------
    def _getInsertParms(self) -> tuple:
        return (
                self.id,                    self.product_id,    self.renter_id,
                self.dropoff_location_id,   self.starts_on,     self.ends_on,
                self.payment_session_id,    self.product_id
        )


        



    











