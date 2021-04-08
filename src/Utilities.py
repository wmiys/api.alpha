import json
import uuid

class Utilities:

    #------------------------------------------------------
    # return the data from the specified json file
    #------------------------------------------------------
    @staticmethod
    def readJsonFile(file_name_path):
        with open(file_name_path) as configFile:
            configData = json.loads(configFile.read())
            return configData
    
    # ------------------------------------------------------
    # Returns a UUID
    #-------------------------------------------------------
    @staticmethod
    def getUUID(as_string: bool=True):
        newUUUID = uuid.uuid4()
        
        if as_string == True:
            return str(newUUUID)
        else:
            return newUUUID
    
    # ------------------------------------------------------
    # Prints a specified number of line breaks to the console
    #-------------------------------------------------------
    @staticmethod
    def lineBreak(num_lines: int=1):
        print("\n" * num_lines)

    # ------------------------------------------------------
    # Prints an object to the console between the specified number of line breaks
    #-------------------------------------------------------
    @staticmethod
    def printWithSpaces(record='', numSpaces: int = 20):
        print("\n" * numSpaces)
        print(record)
        print("\n" * numSpaces)
    
    # ------------------------------------------------------
    # Checks if any of the fields contained in the dict are valid properties of the given object
    #
    # returns a boolean:
    #   true - all dict fields are valid
    #   false - the dict contains a field that is not a property of the object
    #-------------------------------------------------------
    @staticmethod
    def areAllKeysValidProperties(testDict: dict, theObject: object):
        for key in testDict:
            if not hasattr(theObject, key):
                return False
        
        return True

