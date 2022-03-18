from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult

SQL_SELECT_ALL = """
    SELECT  *
    FROM    View_Products p
    WHERE   p.user_id = %s
    GROUP   BY p.id
    ORDER   BY p.name ASC
"""

#------------------------------------------------------
# Retrieve all the user's products
#------------------------------------------------------
def selectAll(user_id) -> DbOperationResult:
    parms = (user_id,)

    return sql_engine.selectAll(SQL_SELECT_ALL, parms)
