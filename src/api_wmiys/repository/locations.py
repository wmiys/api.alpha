"""
**********************************************************************************************

Location respository.

This is an abstraction for all the sql commands related to Locations.

**********************************************************************************************
"""

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult

from api_wmiys.domain import models




#------------------------------------------------------
# Select a single location record
#
# Parms:
#   - location's id
#------------------------------------------------------
SQL_SELECT = """
    SELECT
        id,
        city,
        state_id,
        state_name
    FROM
        Locations l
    WHERE
        l.id = %s
    LIMIT
        1;
"""


#------------------------------------------------------
# Select a single location record from the database
#------------------------------------------------------
def select(location: models.Location) -> DbOperationResult:
    parms = (location.id,)
    return sql_engine.select(SQL_SELECT, parms)