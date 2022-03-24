"""
**********************************************************************************************

Password resets database abstraction. 
Any interaction with the Password_Resets database table should go through here.

**********************************************************************************************
"""

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from pymysql.connection import ConnectionBase
from api_wmiys.domain import models


SQL_INSERT = '''
    INSERT INTO 
        Password_Resets (id, email, created_on) 
    VALUES 
        (%s, %s, %s);
'''


SQL_UPDATE_STORED_PROCEDURE = 'Finalize_Password_Reset'


#----------------------------------------------------------
# Insert the model's values into the database
#----------------------------------------------------------
def insert(password_reset: models.PasswordReset) -> DbOperationResult:
    parms = (
        str(password_reset.id),
        password_reset.email,
        password_reset.created_on,
    )

    return sql_engine.modify(SQL_INSERT, parms)


#----------------------------------------------------------
# Update the user's password
#
# Returns a DbOperationResult:
#   - the data will either have -1 or 1
#       - 1 means it was successful, otherwise it was not
#----------------------------------------------------------
def update(password_reset: models.PasswordReset, num_minutes_expiration: int) -> DbOperationResult:
    result = DbOperationResult(successful=True)
    db = ConnectionBase()

    parms = [
        str(password_reset.id),
        password_reset.updated_on.isoformat(),
        password_reset.password,
        num_minutes_expiration,
    ]

    try:
        db.connect()
        mycursor = db.connection.cursor(dictionary=True)
        mycursor.callproc(SQL_UPDATE_STORED_PROCEDURE, parms)

        # Get the data returned by the stored procedure
        # 1 means successful, otherwise it was not
        returned_data_rs = next(mycursor.stored_results())
        row1             = returned_data_rs.fetchone()
        result.data      = row1.get('rowcount')
        
        db.commit()

    except Exception as e:
        result.successful = False
        result.error = e
        result.data = None
    
    finally:
        db.close()

    return result
