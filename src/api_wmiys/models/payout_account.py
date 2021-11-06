

import uuid
from datetime import datetime

import stripe

from wmiys_common import keys

from ..db import DB, sqlBoolToPython, SqlBool



stripe.api_key = keys.payments.test


def getNewStripeAccount() -> stripe.Account:
    return stripe.Account.create(type='express')



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

    
    def get(self) -> dict:
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = 'SELECT * FROM Payout_Accounts WHERE id=%s LIMIT 1'
        parms = (str(self.id),)
        cursor.execute(sql, parms)
        result = cursor.fetchone()

        db.close()

        result['confirmed'] = sqlBoolToPython(SqlBool(result.get('confirmed')))


        return result   
