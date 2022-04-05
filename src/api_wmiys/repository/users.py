"""

Users repository

"""
from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from pymysql.connection import ConnectionPrepared

from api_wmiys.domain import models



SQL_SELECT = 'SELECT * FROM View_Users WHERE id=%s LIMIT 1;'


SQL_UPDATE = '''
    UPDATE Users 
    SET
        email      = %s,
        password   = %s,
        name_first = %s,
        name_last  = %s,
        birth_date = %s
    WHERE
        id =         %s;
'''



SQL_INSERT = '''
    INSERT INTO 
        Users (email, password, name_first, name_last, birth_date)
    VALUES
        (%s, %s, %s, %s, %s);
'''


#------------------------------------------------------
# Retrieve a single user from the database
#------------------------------------------------------
def select(user: models.User) -> DbOperationResult:
    parms = (user.id,)
    return sql_engine.select(SQL_SELECT, parms)


#------------------------------------------------------
# Update the database's user record to the field values provided in the given User domain model
#------------------------------------------------------
def update(user: models.User) -> DbOperationResult:
    parms = (
        user.email,
        user.password,
        user.name_first,
        user.name_last,
        user.birth_date,
        user.id,
    )


    return sql_engine.modify(SQL_UPDATE, parms)

#------------------------------------------------------
# Insert the user object into the database
#
# Returns: DbOperationResult
#   the DbOperationResult.data value contains the auto-incremented id for the new user
#------------------------------------------------------
def insert(new_user: models.User) -> DbOperationResult:
    result = DbOperationResult(successful=True)
    db = ConnectionPrepared()

    parms = _getInsertParms(new_user)
    
    try:
        db.connect()
        cursor = db.getCursor()
        
        cursor.execute(SQL_INSERT, parms)
        db.commit()
        
        result.data = cursor.lastrowid

    except Exception as e:
        result.error = e
        result.data = None
        result.successful = False
    
    finally:
        db.close()
    
    return result



def _getInsertParms(user: models.User) -> tuple:
    parms = (
        user.email,
        user.password,
        user.name_first,
        user.name_last,
        user.birth_date,
    )

    return parms
