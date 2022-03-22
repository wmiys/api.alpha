"""
**********************************************************************************************

Payout Accounts database abstraction. 
All sql commands regarding payout accounts are here.

**********************************************************************************************
"""

from __future__ import annotations

import pymysql.commands as sql_engine
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models

#------------------------------------------------------
# Select all payout account records that are owned by the user
#
# Parms:
#   - user_id
#------------------------------------------------------
SQL_SELECT_ALL = '''
    SELECT
        *
    FROM
        Payout_Accounts
    WHERE
        user_id = %s
    ORDER BY
        created_on DESC;
'''

#------------------------------------------------------
# Select a single payout account record
#
# Parms:
#   - payout account id
#   - user_id
#------------------------------------------------------
SQL_SELECT = '''
    SELECT
        *
    FROM
        Payout_Accounts
    WHERE
        id = %s
        AND user_id = %s
    LIMIT
        1;
'''


#------------------------------------------------------
# Insert a new record
#
# Parms:
#   - payout account id
#   - user_id
#   - stripe account id
#   - created on
#------------------------------------------------------
SQL_INSERT = '''
    INSERT INTO
        Payout_Accounts (id, user_id, account_id, created_on)
    VALUES
        (%s, %s, %s, %s);
'''


#------------------------------------------------------
# Update a record's confirmed value
#
# Parms:
#   - confirmed
#   - payout account id
#   - user_id
#------------------------------------------------------
SQL_UPDATE = '''
    UPDATE
        Payout_Accounts
    SET
        confirmed = %s
    WHERE
        id = %s
        AND user_id = %s;
'''



#------------------------------------------------------
# Get all payout accounts owned by the given user
#------------------------------------------------------
def selectAll(user_id: int) -> DbOperationResult:
    parms = (user_id,)
    return sql_engine.selectAll(SQL_SELECT_ALL, parms)


#------------------------------------------------------
# Fetch the payout account record with the matching id as the one given in the domain model
#------------------------------------------------------
def select(payout_account: models.PayoutAccount) -> DbOperationResult:
    parms = (
        str(payout_account.id),
        payout_account.user_id,
    )

    return sql_engine.select(SQL_SELECT, parms)

#------------------------------------------------------
# Insert the given payout account into the database
#------------------------------------------------------
def insert(payout_account: models.PayoutAccount) -> DbOperationResult:    
    parms = (
        str(payout_account.id), 
        payout_account.user_id, 
        payout_account.account_id, 
        payout_account.created_on
    )

    return sql_engine.modify(SQL_INSERT, parms)


#------------------------------------------------------
# Update the given payout account object in the database
#------------------------------------------------------
def update(payout_account: models.PayoutAccount) -> DbOperationResult:
    parms = (
        payout_account.confirmed,
        str(payout_account.id),
        payout_account.user_id,
    )

    return sql_engine.modify(SQL_UPDATE, parms)