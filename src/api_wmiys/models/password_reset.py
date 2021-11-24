"""
**********************************************************************************************

Represents a password reset object. 

**********************************************************************************************
"""
from datetime import datetime
from uuid import UUID

from ..db import DB, DbCommand

class PasswordReset:

    def __init__(self, id: UUID=None, user_email: str=None, created_on: datetime=None, new_password: str=None, updated_on: datetime=None):
        self.id           = id
        self.user_email   = user_email
        self.created_on   = created_on
        self.new_password = new_password
        self.updated_on   = updated_on


    def insert(self) -> DbCommand:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'INSERT INTO Password_Resets (id, user_email) VALUES (%s, %s)'
        parms = (str(self.id), self.user_email)

        db_command = DbCommand(successful=False)

        try:
            cursor.execute(sql, parms)
            db.commit()

            db_command.result = cursor.rowcount
            db_command.successful = True
        except Exception as e:
            db_command.error = e
        finally:
            db.close()
        
        return db_command

            






    
