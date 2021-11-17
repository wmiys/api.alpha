"""
**********************************************************************************************
This class represents a balance transfer. 
Balance transfers occur when a lender wants to transfer their earnings to their bank account.
Lenders need to have a balance greater than 1 in order to successfully transfer their balance.
**********************************************************************************************
"""

from uuid import UUID
from datetime import datetime
import stripe
from wmiys_common import keys, utilities
from ..db import DB


stripe.api_key = keys.payments.test


class BalanceTransfer:
    """Balance Transfers"""

    #------------------------------------------------------
    # Constructor
    #------------------------------------------------------
    def __init__(self, id: UUID=None, user_id: int=None, amount: float=0, created_on: datetime=None, destination_account_id: str=None, transfer_id: str=None):
        self.id                     = id
        self.user_id                = user_id
        self.amount                 = amount
        self.created_on             = created_on
        self.destination_account_id = destination_account_id
        self.transfer_id            = transfer_id

    #------------------------------------------------------
    # Tell stripe to send a lender their current balance
    #------------------------------------------------------
    def sendTransfer(self) -> bool:
        
        try:
            transfer_obj: stripe.Transfer = stripe.Transfer.create(
                amount         = utilities.dollarsToCents(self.amount),
                currency       = "usd",
                destination    = self.destination_account_id,
            )

            self.transfer_id = transfer_obj.id

            result = True
        except Exception as e:
            print(e)
            result = False   
        
        return result

    #------------------------------------------------------
    # Record the transfer in the database
    #------------------------------------------------------ 
    def insert(self):
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'INSERT INTO Balance_Transfers (id, user_id, amount, destination_account_id, transfer_id) VALUES (%s, %s, %s, %s, %s)'
        parms = (str(self.id), self.user_id, self.amount, self.destination_account_id, self.transfer_id)
        
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


