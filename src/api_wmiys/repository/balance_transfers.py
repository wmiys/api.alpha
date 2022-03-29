"""
**********************************************************************************************

Balance transfers sql commands.

**********************************************************************************************
"""

from __future__ import annotations
import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models


SQL_INSERT = '''
    INSERT INTO 
        Balance_Transfers (id, user_id, amount, destination_account_id, transfer_id, created_on) 
    VALUES 
        (%s, %s, %s, %s, %s, %s);
'''


#------------------------------------------------------
# Insert the transfer in the database
#------------------------------------------------------
def insert(bt: models.BalanceTransfer) -> DbOperationResult:
    parms = _getInsertParms(bt)
    return sql_engine.modify(SQL_INSERT, parms)

#------------------------------------------------------
# Get the insert command parms tuple
#------------------------------------------------------
def _getInsertParms(balance_transfer: models.BalanceTransfer) -> tuple:
    parms = (
        str(balance_transfer.id),
        balance_transfer.user_id,
        balance_transfer.amount,
        balance_transfer.destination_account_id,
        balance_transfer.transfer_id,
        balance_transfer.created_on,
    )

    return parms
