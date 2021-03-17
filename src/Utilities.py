import json

class Utilities:

    # return the data from the local .tables.config file
    @staticmethod
    def readJsonFile(file_name_path):
        with open(file_name_path) as configFile:
            configData = json.loads(configFile.read())
            return configData