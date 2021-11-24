"""
**********************************************************************************************

Represents a password reset object. 

**********************************************************************************************
"""
from datetime import datetime
from uuid import UUID
from ..db import DB, DbCommand

class PasswordReset:

    def __init__(self, id: UUID=None, email: str=None, created_on: datetime=None, new_password: str=None, updated_on: datetime=None):
        self.id           = id
        self.email   = email
        self.created_on   = created_on
        self.new_password = new_password
        self.updated_on   = updated_on


    #------------------------------------------------------
    # Insert a new record into the database.
    #------------------------------------------------------
    def insert(self) -> DbCommand:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'INSERT INTO Password_Resets (id, email) VALUES (%s, %s)'
        parms = (str(self.id), self.email)

        db_command = DbCommand(successful=False)

        try:
            cursor.execute(sql, parms)
            db.commit()

            db_command.result = cursor.rowcount
            db_command.successful = True
        except Exception as e:
            db_command.error = str(e)
        finally:
            db.close()
        
        return db_command

    #------------------------------------------------------
    # Retrieve a password reset record
    #------------------------------------------------------
    def get(self) -> DbCommand:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = 'SELECT * FROM Password_Resets WHERE id = %s LIMIT 1'
        parms = (str(self.id),)

        db_command = DbCommand(successful=False)

        try:
            cursor.execute(sql, parms)
            db_command.result = cursor.fetchone()
            db_command.successful = True
        except Exception as e:
            db_command.successful = False
            db_command.error = str(e)
        finally:
            db.close()
        
        return db_command








    
