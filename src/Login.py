from DB import DB

class Login:

    @staticmethod
    def isValidLoginAttempt(email: str, password: str):
        result = DB.getUserIDFromEmailPassword(email, password)

        if result == None:
            return None
        else:
            return result.id


