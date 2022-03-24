"""
**********************************************************************************************

Password resets database abstraction. 
Any interaction with the Password_Resets database table should go through here.

**********************************************************************************************
"""

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models

from api_wmiys.domain import models


SQL_INSERT = '''
    INSERT INTO 
        Password_Resets (id, email, created_on) 
    VALUES 
        (%s, %s, %s);
'''



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
