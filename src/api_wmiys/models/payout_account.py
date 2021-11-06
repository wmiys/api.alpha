

import uuid
from datetime import datetime

import stripe

from wmiys_common import keys
from ..db import DB



stripe.api_key = keys.payments.test


def getNewStripeAccount() -> stripe.Account:
    return stripe.Account.create(type='express')



class PayoutAccount:

    def __init__(self, id: uuid.UUID=None, user_id: int=None, account_id: str=None, created_on: datetime=None, confirmed: bool=False):
        self.id         = id
        self.user_id    = user_id
        self.account_id = account_id
        self.created_on = created_on
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

        sql = 'INSERT INTO Payout_Accounts (id, user_id, account_id) VALUES (%s, %s, %s)'
        parms = (str(self.id), self.user_id, self.account_id)

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
        
