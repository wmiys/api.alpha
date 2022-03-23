"""

Users repository

"""

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models



SQL_SELECT = 'SELECT * FROM View_Users WHERE id=%s LIMIT 1;'

#------------------------------------------------------
# Retrieve a single user from the database
#------------------------------------------------------
def select(user: models.User) -> DbOperationResult:
    parms = (user.id,)
    return sql_engine.select(SQL_SELECT, parms)







