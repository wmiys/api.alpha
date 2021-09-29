from ..db import DB
import datetime

class ProductRequest:

    #-----------------------------------------------------
    # Constrcutor
    # ----------------------------------------------------
    def __init__(self, id: int=None, renter_id: int=None, product_id: int=None, starts_on: datetime.date=None, ends_on: datetime.date=None, dropoff_location_id: int=None):
        self.id                  = id
        self.renter_id           = renter_id
        self.product_id          = product_id
        self.starts_on           = starts_on
        self.ends_on             = ends_on
        self.dropoff_location_id = dropoff_location_id

    #-----------------------------------------------------
    # Insert the object into the database
    #
    # Returns a bool: whether or not it was successful
    # ----------------------------------------------------
    def insert(self):
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = '''
        INSERT INTO Product_Requests (renter_id, product_id, starts_on, ends_on, dropoff_location_id, price_full, price_half) 
            SELECT
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    p.price_full,
                    p.price_half
            FROM    Products p 
            WHERE   p.id = %s;
        '''

        parms = (self.renter_id, self.product_id, self.starts_on, self.ends_on, self.dropoff_location_id, self.product_id)

        try:
            cursor.execute(sql, parms)
            db.commit()
            self.id = cursor.lastrowid
            successful = True
        except Exception as e:
            successful = False
            print(e)
        finally:
            db.close()
        
        return successful


    #-----------------------------------------------------
    # Checks if all the required properties needed to insert
    # the request have a value.
    #
    # The required properties are:
    #   - renter_id
    #   - product_id
    #   - starts_on
    #   - ends_on
    #   - dropoff_location_id
    # ----------------------------------------------------
    def allPropertiesForInsertSet(self) -> bool:
        if None in [self.renter_id, self.product_id, self.starts_on, self.ends_on, self.dropoff_location_id]:
            return False
        else:
            return True


