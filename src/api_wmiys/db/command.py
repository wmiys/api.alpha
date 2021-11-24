"""
**********************************************************************************************

A DbCommand is the result of an database command. Whether it's a select, insert, update, or 
delete. All models that execute a command should return one of these.

**********************************************************************************************
"""


class DbCommand:

    def __init__(self, result=None, successful: bool=True, error: str=None):
        self.result     = result
        self.successful = successful
        self.error      = error
