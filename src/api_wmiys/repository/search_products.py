
from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models
from api_wmiys.common import Sorting


from wmiys_common import utilities

_SQL_STMT_PREFIX = '''
    SELECT * FROM View_Search_Products p
    WHERE SEARCH_PRODUCTS_FILTER(p.id, %s, %s, %s) = TRUE 
'''


def selectAll(product_search: models.ProductSearchRequest) -> DbOperationResult:
    sql = _getStmtWithLimit(product_search)
    parms = _getSelectAllParms(product_search)

    return sql_engine.selectAll(sql, parms)


# create the sql statement to calculate the count
def selectAllTotalCount(product_search: models.ProductSearchRequest) -> DbOperationResult:
    sql = _getStmtTotalCount(product_search)
    parms = _getSelectAllParms(product_search)

    return sql_engine.select(sql, parms)




def _getStmtWithLimit(product_search: models.ProductSearchRequest) -> str:
    prefix = _getStmtPrefix(product_search.sorting)
    sql    = product_search.pagination.getSqlStmtLimitOffset(prefix)
    result = f'{sql};'

    return result


def _getStmtTotalCount(product_search: models.ProductSearchRequest) -> str:
    prefix  = _getStmtPrefix(product_search.sorting)
    sql = product_search.pagination.getSqlStmtTotalCount(prefix)
    
    return f'{sql};'


def _getStmtPrefix(sorting: Sorting) -> str:
    return f'{_SQL_STMT_PREFIX} ORDER BY {sorting.field} {sorting.type}'



def _getSelectAllParms(product_search: models.ProductSearchRequest) -> tuple:
    parms = (
        product_search.location_id, 
        product_search.starts_on, 
        product_search.ends_on
    )

    return parms




