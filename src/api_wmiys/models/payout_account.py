"""
**********************************************************************************************
Payout Accounts represent the lender's connected account on stripe. 

Before users can start lending their products, they need to setup an account with stripe.

This is so we can pay out their account balance to their bank account after successfully 
lending out their products. 
**********************************************************************************************
"""
from __future__ import annotations
import uuid
from datetime import datetime
import stripe
from wmiys_common import keys
from ..db import DB, sqlBoolToPython, SqlBool


stripe.api_key = keys.payments.test

#------------------------------------------------------
# Create a new stripe account
#------------------------------------------------------
def getNewStripeAccount(user_id: int) -> stripe.Account:
    
    return stripe.Account.create(
        type='express',
        metadata=dict(user_id=user_id)
    )

#------------------------------------------------------
# Get all payout accounts owned by the given user
#------------------------------------------------------
def getAll(user_id: int) -> list[dict]:
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    sql = 'SELECT * FROM Payout_Accounts WHERE user_id=%s ORDER BY created_on DESC'
    parms = (user_id,)
    cursor.execute(sql, parms)
    records: list = cursor.fetchall()

    db.close()

    # transform all sql bool types into python bools
    for i, record in enumerate(records):
        records[i]['confirmed'] = sqlBoolToPython(SqlBool(record.get('confirmed')))
    
    return records


class PayoutAccount:

    def __init__(self, id: uuid.UUID=None, user_id: int=None, account_id: str=None, created_on: datetime=None, confirmed: bool=False):
        self.id         = id
        self.user_id    = user_id
        self.account_id = account_id
        self.created_on = created_on or datetime.now()
        self.confirmed  = confirmed

    #------------------------------------------------------
    # Insert the object into the database
    #
    # Returns a bool:
    #   true: insert was successful
    #   false: insert was not successful
    #------------------------------------------------------
    def insert(self) -> bool:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'INSERT INTO Payout_Accounts (id, user_id, account_id, created_on) VALUES (%s, %s, %s, %s)'
        parms = (str(self.id), self.user_id, self.account_id, self.created_on)

        try:
            cursor.execute(sql, parms)
            db.commit()
            success = True
        except Exception as e:
            success = False
            print(e)
        finally:
            db.close()
        
        return success




    def load(self):
        db_result = self.get()

        if not db_result:
            return False

        # self.id         = db_result.get('id')
        self.user_id    = db_result.get('user_id')
        self.account_id = db_result.get('account_id')
        self.created_on = db_result.get('created_on')
        self.confirmed  = db_result.get('confirmed')

        return True


    #------------------------------------------------------
    # Get a single payout account
    #------------------------------------------------------
    def get(self) -> dict:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = 'SELECT * FROM Payout_Accounts WHERE id=%s and user_id=%s LIMIT 1'
        parms = (str(self.id), self.user_id)
        cursor.execute(sql, parms)
        result = cursor.fetchone()

        db.close()

        if result:
            result['confirmed'] = sqlBoolToPython(SqlBool(result.get('confirmed')))

        return result

    #------------------------------------------------------
    # Update the object
    #------------------------------------------------------
    def update(self) -> int:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'UPDATE Payout_Accounts SET confirmed = %s WHERE id=%s and user_id=%s'
        parms = (self.confirmed, str(self.id), self.user_id)

        try:
            cursor.execute(sql, parms)
            db.commit()
            row_count = cursor.rowcount
        except Exception as e:
            print(e)
            row_count = -1
        finally:
            db.close()

        return row_count

