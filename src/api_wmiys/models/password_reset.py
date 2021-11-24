"""
**********************************************************************************************

Represents a password reset object. 

**********************************************************************************************
"""
from __future__ import annotations
from datetime import datetime
from http import HTTPStatus
from typing import NamedTuple, Tuple
from uuid import UUID
import flask
from wmiys_common import utilities
from ..db import DB, DbCommand



NUM_MINS_EXPIRED = 30


class PasswordReset:

    def __init__(self, id: UUID=None, email: str=None, created_on: datetime=None, new_password: str=None, updated_on: datetime=None):
        self.id           = id
        self.email        = email
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
    # Laod up the object's attributes with the db record values
    #------------------------------------------------------
    def load(self) -> DbCommand:
        
        result = DbCommand(successful=True)
        
        db_result = self.get()

        if not db_result.successful:
            result.successful = False
            result.error = db_result.error
            return result
        
        self.email        = db_result.result.get('email') or None
        self.created_on   = db_result.result.get('created_on') or None
        self.new_password = db_result.result.get('new_password') or None
        self.updated_on   = db_result.result.get('updated_on') or None

        return result


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


    def update(self) -> DbCommand:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'UPDATE Password_Resets SET new_password=%s, updated_on=CURRENT_TIMESTAMP() WHERE id=%s'
        parms = (self.new_password, str(self.id))

        db_command = DbCommand(successful=True)

        try:
            cursor.execute(sql, parms)
            db.commit()
            db_command.result = cursor.rowcount
        except Exception as e:
            db_command.successful = False
            db_command.error = str(e)
        finally:
            db.close()

        if not db_command.successful:
            return db_command
        
        # now update the user's account password
        return self._updateUser()
        


    def _updateUser(self) -> DbCommand:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'UPDATE Users SET password=%s where email=%s'
        parms = (self.new_password, self.email)

        db_command = DbCommand(successful=True)

        try:
            cursor.execute(sql, parms)
            db.commit()
            db_command.result = cursor.rowcount
        except Exception as e:
            db_command.successful = False
            db_command.error = str(e)
        finally:
            db.close()
        
        return db_command


    def canPasswordBeReset(self) -> flask.Response | None:
        # make sure the id exists
        if not self.email:
            return ('ID does not exist', HTTPStatus.NOT_FOUND.value)

        if not self.isUpdateable():
            return ('Invalid password reset id.', HTTPStatus.BAD_REQUEST)
        
        if self.isExpired():
            return ('Request has expired.', HTTPStatus.BAD_REQUEST)
        
        return None


    def isUpdateable(self) -> bool:
        if not self.updated_on:
            return True


    def isExpired(self) -> bool:
        num_minutes = utilities.getDurationMinutes(self.created_on, datetime.now())

        if num_minutes <= NUM_MINS_EXPIRED:
            return False
        else:
            return True

        







    
