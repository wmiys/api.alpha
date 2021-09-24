from api_wmiys.DB.DB import DB

class Login:
    
    @staticmethod
    def getUserID(email: str, password: str):
        """Get a userID from an email/password combination

        Args:
            email (str): user emai
            password (str): user  

        Returns:
            Either the user id or None
        """
        result = DB.getUserIDFromEmailPassword(email, password)

        if result == None:
            return result
        else:
            return int(result.id)


