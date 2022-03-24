
from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_SELECT_ALL = '''
    SELECT   *
    FROM     View_Product_Availability pa
    WHERE    pa.product_id = %s
    ORDER BY pa.created_on DESC;
'''


SQL_MODIFY = '''
    INSERT INTO
        Product_Availability (id, product_id, starts_on, ends_on, note)
    VALUES
        (%s, %s, %s, %s, %s) AS new_values 
    ON DUPLICATE KEY UPDATE
        starts_on = new_values.starts_on,
        ends_on = new_values.ends_on,
        note = new_values.note;
'''



#------------------------------------------------------
# Returns all product availability records for a single product
#
# Parms:
#   product_id - the product id
#
# Returns: list of product availability records
#------------------------------------------------------
def selectAll(product_id) -> DbOperationResult:
    parms = (product_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)


#------------------------------------------------------
# Insert the product availability into the database
#------------------------------------------------------
def insert(product_availability: models.ProductAvailability) -> DbOperationResult:
    parms = (
        str(product_availability.id),
        product_availability.product_id,
        product_availability.starts_on,
        product_availability.ends_on,
        product_availability.note,
    )

    return sql_engine.modify(SQL_MODIFY, parms)

