import json

class Utilities:

    @staticmethod
    def getJsonData(fileName):
        inputFile = open(fileName, 'r')
        jsonData = json.loads(inputFile.read())
        inputFile.close()

        return jsonData

    @staticmethod
    def writeJsonToFile(outputData, fileName):
        jsonString = json.dumps(outputData, sort_keys=True, indent=4)

        with open(fileName, "w") as outputFile:
            outputFile.write(jsonString)