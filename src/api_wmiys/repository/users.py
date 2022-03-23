"""

Users repository

"""
from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models



SQL_SELECT = 'SELECT * FROM View_Users WHERE id=%s LIMIT 1;'


SQL_UPDATE = """
    UPDATE Users 
    SET
        email      = %s,
        password   = %s,
        name_first = %s,
        name_last  = %s,
        birth_date = %s
    WHERE
        id =         %s;
"""


#------------------------------------------------------
# Retrieve a single user from the database
#------------------------------------------------------
def select(user: models.User) -> DbOperationResult:
    parms = (user.id,)
    return sql_engine.select(SQL_SELECT, parms)



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





