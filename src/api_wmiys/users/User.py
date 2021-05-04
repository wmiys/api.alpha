#************************************************************************************
#
# This class handles all the requests for a single user.
#
#************************************************************************************

from api_wmiys.DB.DB import DB
from api_wmiys.common.Utilities import Utilities

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
        user_id = DB.insert_user(email=self.email, password=self.password, name_first=self.name_first, name_last=self.name_last, birth_date=self.birth_date)
        self.id = user_id

    #------------------------------------------------------
    # Retrieve the user info from the database
    #------------------------------------------------------
    def fetch(self):
        # don't do anything if the user id isn't set
        if self.id is None:
            return
                
        db_data = DB.get_user(self.id)

        self.email      = db_data.email
        self.password   = db_data.password
        self.name_first = db_data.name_first
        self.name_last  = db_data.name_last
        self.birth_date = db_data.birth_date
        self.created_on = db_data.created_on
    
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
        if not Utilities.areAllKeysValidProperties(newPropertyValues, self):
            return False

        # set the object properties
        for key in newPropertyValues:
            if newPropertyValues[key]:
                setattr(self, key, newPropertyValues[key])
            else:
                setattr(self, key, None)
            
        return True
    
    #------------------------------------------------------
    # update the database to the field values currently in the object
    #------------------------------------------------------
    def update(self):
        if not self.id:
            return 0

        updateResult = DB.update_user(id=self.id, email=self.email, password=self.password, name_first=self.name_first, name_last=self.name_last, birth_date=self.birth_date)

        return updateResult.rowcount





        

