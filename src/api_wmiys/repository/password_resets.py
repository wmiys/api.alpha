"""
**********************************************************************************************

Password resets database abstraction. 
Any interaction with the Password_Resets database table should go through here.

**********************************************************************************************
"""

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from pymysql.connection import ConnectionPrepared, ConnectionBase, ConnectionDict
from api_wmiys.domain import models

from api_wmiys.domain import models


SQL_INSERT = '''
    INSERT INTO 
        Password_Resets (id, email, created_on) 
    VALUES 
        (%s, %s, %s);
'''


SQL_UPDATE = '''
    UPDATE
        Password_Resets pr
    SET
        pr.updated_on = %s
    WHERE
        pr.id = %s
        AND pr.updated_on IS NULL
        AND ABS(
            TIMESTAMPDIFF(MINUTE, pr.created_on, %s)
        ) <= {MAX_MINUTES};
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
# Insert the model's values into the database
#----------------------------------------------------------
def update(password_reset: models.PasswordReset, num_minutes_expiration: int) -> DbOperationResult:
    result = DbOperationResult(successful=True)

    print(password_reset)

    db = ConnectionDict()

    parms = [
        str(password_reset.id),
        password_reset.updated_on,
        password_reset.password,
        num_minutes_expiration
    ]

    # print(parms)

    try:
        db.connect()
        mycursor = db.getCursor()
        
        # call the stored procedure
        mycursor.callproc(SQL_UPDATE_STORED_PROCEDURE, parms)
        
        # fetch the results from the cursor
        stored_results = next(mycursor.stored_results())
        first_row = stored_results.fetchone()
        print(first_row)
        result.data = first_row.get('rowcount')
        
    except Exception as e:
        result.successful = False
        result.error = e
        result.data = None
    
    finally:
        db.close()

    return result
