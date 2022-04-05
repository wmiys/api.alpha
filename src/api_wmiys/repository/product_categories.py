"""
**********************************************************************************************

All the sql commands for fetching product categories.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult


SQL_SELECT_ALL = '''
    SELECT 
        *
    FROM
        All_Categories;
'''


SQL_SELECT_ALL_MAJORS = '''
    SELECT
        major.id AS id,
        major.name AS name
    FROM
        Product_Categories_Major major
    ORDER BY
        major.name ASC;
'''

SQL_SELECT_MAJOR = '''
    SELECT
        major.id AS id,
        major.name AS name
    FROM
        Product_Categories_Major major
    WHERE
        major.id = %s
    LIMIT
        1;
'''

SQL_SELECT_ALL_MINORS = '''
    SELECT
        minor.id AS id,
        minor.product_categories_major_id AS product_categories_major_id,
        minor.name AS name
    FROM
        Product_Categories_Minor minor
    WHERE
        minor.product_categories_major_id = %s
    GROUP   BY
        minor.id
    ORDER   BY
        minor.name ASC;
'''

SQL_SELECT_MINOR = '''
    SELECT
        minor.id AS id,
        minor.product_categories_major_id AS product_categories_major_id,
        minor.name AS name
    FROM
        Product_Categories_Minor minor
    WHERE
        minor.id = %s
    LIMIT
        1;
'''

SQL_SELECT_ALL_SUBS = '''
    SELECT
        s.id AS id,
        s.product_categories_minor_id AS product_categories_minor_id,
        s.name AS name
    FROM
        Product_Categories_Sub s
    WHERE
        s.product_categories_minor_id = %s
    GROUP   BY
        s.id
    ORDER   BY
        s.name ASC;
'''

SQL_SELECT_SUB = '''
    SELECT
        s.id AS id,
        s.product_categories_minor_id AS product_categories_minor_id,
        s.name AS name
    FROM
        Product_Categories_Sub s
    WHERE
        s.id = %s
    LIMIT
        1;
'''



#------------------------------------------------------
# Get all the product categories
#------------------------------------------------------
def selectAll() -> DbOperationResult:
    return sql_engine.selectAll(SQL_SELECT_ALL)


#------------------------------------------------------
# Retrieve all major categories
#------------------------------------------------------
def selectMajors() -> DbOperationResult:
    return sql_engine.selectAll(SQL_SELECT_ALL_MAJORS)

#------------------------------------------------------
# Retrieve a single major category
#------------------------------------------------------
def selectMajor(major_category_id) -> DbOperationResult:
    parms = (major_category_id,)
    return sql_engine.select(SQL_SELECT_MAJOR, parms)

#------------------------------------------------------
# Retrieve all minor categories under the given major id
#------------------------------------------------------
def selectMinors(parent_category_id) -> DbOperationResult:
    parms = (parent_category_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL_MINORS, parms)

#------------------------------------------------------
# Retrieve a single minor category
#------------------------------------------------------
def selectMinor(minor_category_id) -> DbOperationResult:
    parms = (minor_category_id,)
    return sql_engine.select(SQL_SELECT_MINOR, parms)

#------------------------------------------------------
# Retrieve all major categories
#------------------------------------------------------
def selectSubs(parent_category_id) -> DbOperationResult:
    parms = (parent_category_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL_SUBS, parms)

#------------------------------------------------------
# Retrieve a single sub category
#------------------------------------------------------
def selectSub(sub_category_id) -> DbOperationResult:
    parms = (sub_category_id,)
    return sql_engine.select(SQL_SELECT_SUB, parms)


