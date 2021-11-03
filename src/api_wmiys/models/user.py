#************************************************************************************
#
# This class handles all the requests for a single user.
#
#************************************************************************************

from wmiys_common import utilities
from ..db import DB


class User:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id=None,email=None,password=None,name_first=None,name_last=None,birth_date=None,created_on=None):
        self.id         = id
        self.email      = email
        self.password   = password
        self.name_first = name_first
        self.name_last  = name_last
        self.birth_date = birth_date
        self.created_on = created_on

    #------------------------------------------------------
    # Returns the user object as a string
    #------------------------------------------------------
    def __str__(self):
        output = ''

        for key, value in self.__dict__:
            output += "\n{}: {}".format(key, value)    

        return output

    #------------------------------------------------------
    # Insert the user object into the database
    #------------------------------------------------------
    def insert(self):        
        db = DB()
        db.connect()

        cursor = db.getCursor(False)

        sql = """
        INSERT INTO Users 
        (email, password, name_first, name_last, birth_date) VALUES
        (%s, %s, %s, %s, %s)
        """

        parm_values = (self.email, self.password, self.name_first, self.name_last, self.birth_date)
        cursor.execute(sql, parm_values)

        db.commit()
        self.id = cursor.lastrowid
        
        db.close()


    

    #------------------------------------------------------
    # Retrieve the user info from the database
    #------------------------------------------------------
    def fetch(self):
        # don't do anything if the user id isn't set
        if self.id is None:
            return

        db = DB()
        db.connect()
        cursor = db.getCursor(asDict=True)

        sql = """
        SELECT 
            u.id as id,
            u.email as email,
            u.password as password,
            u.name_first as name_first,
            u.name_last as name_last,
            u.created_on as created_on,
            DATE_FORMAT(u.birth_date, '%Y-%m-%d') as birth_date
        FROM Users u
        WHERE 
            u.id = %s
        LIMIT 1
        """
        parms = (self.id,)
        
        cursor.execute(sql, parms)
        record_set: dict = cursor.fetchone()

        self.email      = record_set.get('email', None)
        self.password   = record_set.get('password', None)
        self.name_first = record_set.get('name_first', None)
        self.name_last  = record_set.get('name_last', None)
        self.birth_date = record_set.get('birth_date', None)
        self.created_on = record_set.get('created_on', None)

        db.close()

    

    #------------------------------------------------------
    # update the database to the field values currently in the object
    #------------------------------------------------------
    def update(self):
        if not self.id:
            return 0

        db = DB()
        db.connect()
        cursor = db.getCursor(asDict=False)

        parms = (self.email, self.password, self.name_first, self.name_last, self.birth_date, self.id)

        sql = """
        UPDATE Users 
        SET
            email = %s,
            password   = %s,
            name_first = %s,
            name_last  = %s,
            birth_date = %s
        WHERE
            id = %s
        """

        cursor.execute(sql, parms)
        db.commit()

        row_count = cursor.rowcount

        db.close()

        return row_count
    

    #------------------------------------------------------
    # return the object as a dict without the password
    #------------------------------------------------------
    def as_dict(self, return_password=False):
        # create a dict from the user fields
        result = self.__dict__

        if return_password == False:
            del result['password']      # remove the password field

        return result
    
    #------------------------------------------------------
    # set the property values of the object to the dict passed in.
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
    






        

