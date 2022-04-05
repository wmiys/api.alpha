"""
**********************************************************************************************

Search locations sql interface

**********************************************************************************************
"""

from __future__ import annotations
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models
from pymysql.connection import ConnectionDict

SEARCH_STORED_PROCEDURE = 'Search_Locations'

#------------------------------------------------------
# Call the search location sql stored procedure
#------------------------------------------------------
def selectAll(search: models.SearchLocations) -> DbOperationResult:
    parms = [
        search.query, 
        search.per_page
    ]

    db_result = DbOperationResult(successful=True)
    db = ConnectionDict()

    try:
        # connect to the database
        db.connect()
        mycursor = db.getCursor()

        # call the stored procedure
        mycursor.callproc(SEARCH_STORED_PROCEDURE, parms)

        # get the record set handle (the first one)
        record_set = next(mycursor.stored_results())    

        # fetch all the records
        db_result.data = record_set.fetchall()

    except Exception as e:
        db_result.successful = False
        db_result.data       = None
        db_result.error      = e
    
    finally:
        db.close()
    
    return db_result
