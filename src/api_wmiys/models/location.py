"""
**********************************************************************************************
A location is used to pin point an address. 

Lenders give their products a location value. This determines how far out they are willing
to drop off their products to a renter. Or, lenders' products will only show up in the search
results if their product's location and dropoff distance fall within the searchers dropoff 
location.
**********************************************************************************************
"""

from ..db import DB

class Location:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id: int=None, city: str=None, state_id: str=None, state_name: str=None):
        self.id = id
        self.city = city
        self.state_id = state_id
        self.state_name = state_name

    #------------------------------------------------------
    # Load the object's properties from the database 
    #------------------------------------------------------
    def load(self) -> bool:
        if not self.id:
            return False


        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = """
        SELECT id, city, state_id, state_name
        FROM Locations l
        WHERE l.id = %s
        LIMIT 1
        """

        parms = (self.id,)
        cursor.execute(sql, parms)
        record_set = cursor.fetchone()

        self.city       = record_set.get('city', None)
        self.state_id   = record_set.get('state_id', None)
        self.state_name = record_set.get('state_name', None)

        db.close()

        return True
    
    #------------------------------------------------------
    # Transform the object into a dict
    #------------------------------------------------------
    def toDict(self) -> dict:
        resultDict = dict(id=self.id, city = self.city, state_id = self.state_id, state_name = self.state_name)
        return resultDict
