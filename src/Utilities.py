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
    #------------------------------------------------------
    @staticmethod
    def getUUID(as_string: bool=True):
        newUUUID = uuid.uuid4()
        
        if as_string == True:
            return str(newUUUID)
        else:
            return newUUUID
    
    @staticmethod
    def lineBreak(num_lines: int=1):
        print("\n" * num_lines)

    @staticmethod
    def printWithSpaces(record='', numSpaces: int = 20):
        print("\n" * numSpaces)
        print(record)
        print("\n" * numSpaces)
    
    @staticmethod
    def areAllKeysValidProperties(testDict: dict, theObject: object):
        for key in testDict:
            if not hasattr(theObject, key):
                return False
        
        return True

