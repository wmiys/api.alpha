"""
Globals

This class contains global values that are shared throughout a request.
"""

class Globals:

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, client_id=None):
        self.client_id = client_id
