from __future__ import annotations
from enum import Enum
from ..db import DB


#-----------------------------------------------------
# Retrieve all the requests that a lender has received.
# 
# Parms:
#   lender_id - the lender's user_id
# ----------------------------------------------------
def getReceivedAll(lender_id) -> list[dict]:
    sql = '''
        SELECT * 
        FROM View_Requests_Lender v 
        WHERE v.product_id IN (SELECT id FROM Products p WHERE p.user_id = %s)
    '''

    parms = (lender_id,)

    return _getReceivedLenderBase(sql, parms)


#-----------------------------------------------------
# Retrieve all the requests that a lender has received.
# 
# Parms:
#   lender_id - the lender's user_id
# ----------------------------------------------------
def getReceivedFilterByStatus(lender_id, status: RequestStatus) -> list[dict]:
    sql = '''
        SELECT * 
        FROM View_Requests_Lender v 
        WHERE 
            v.product_id IN (SELECT id FROM Products p WHERE p.user_id = %s) 
            AND v.status = %s 
    '''

    parms = (lender_id, status.value)

    return _getReceivedLenderBase(sql, parms)





def _getReceivedLenderBase(sql: str, parms: tuple):
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    cursor.execute(sql, parms)
    requests = cursor.fetchall()
    
    db.close()

    return requests


#-----------------------------------------------------
# This is the different type of status' a request can have.
# ----------------------------------------------------
class RequestStatus(str, Enum):
    pending  = 'pending'
    accepted = 'accepted'
    denied   = 'denied'
    expired  = 'expired'


    @staticmethod
    def getStatus(status: str) -> RequestStatus:
        if status == RequestStatus.expired.value:
            return RequestStatus.expired
        elif status == RequestStatus.accepted.value:
            return RequestStatus.accepted
        elif status == RequestStatus.denied.value:
            return RequestStatus.denied
        elif status == RequestStatus.pending.value:
            return RequestStatus.pending
        else:
            return None


class ProductRequest:

    #-----------------------------------------------------
    # Constructor
    # ----------------------------------------------------
    def __init__(self, id=None, payment_id=None, session_id=None, status=RequestStatus.pending, responded_on=None, created_on=None):
        self.id           = id
        self.payment_id   = payment_id
        self.session_id   = session_id
        self.status       = status
        self.responded_on = responded_on
        self.created_on   = created_on

    #-----------------------------------------------------
    # Retrieve a lender's request from the database
    # ----------------------------------------------------
    def getLender(self) -> dict:
        if not self.id:
            return None
        
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = '''
            SELECT * 
            FROM View_Requests_Lender v 
            WHERE v.id = %s
        '''

        parms = (self.id,)

        try:
            cursor.execute(sql, parms)
            request = cursor.fetchone()
        except Exception as e:
            request = None
            print(e)
        finally:
            db.close()

        return request


    #-----------------------------------------------------
    # Verifies that all the required object attributes are 
    # valid in order to insert the object into the database.
    # 
    # Returns a bool:
    #   true - all attributes are set
    #   false - one of the attributes are not set
    # ----------------------------------------------------
    def areInsertAttributesSet(self) -> bool:
        if None in [self.payment_id, self.session_id]:
            return False
        else:
            return True

    #-----------------------------------------------------
    # Insert the object into the database
    #
    # Returns a bool: whether or not it was successful
    # ----------------------------------------------------
    def insert(self) -> bool:
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = 'INSERT INTO Product_Requests (payment_id, session_id) VALUES (%s, %s)'
        parms = (self.payment_id, self.session_id)

        successful = True

        try:
            cursor.execute(sql, parms)
            db.commit()
            self.id = cursor.lastrowid
        except Exception as e:
            print(e)
            successful = False
        finally:
            db.close()

        return successful

    #-----------------------------------------------------
    # Set the object's attributes from the database record 
    # data.
    #
    # Returns a bool: whether or not it was successful
    # ----------------------------------------------------
    def load(self) -> bool:
        if not self.id:
            return False
        
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = '''
        SELECT  payment_id, 
                session_id, 
                status, 
                responded_on, 
                created_on 
        FROM    Product_Requests 
        WHERE   id = %s
        LIMIT   1
        '''
        cursor.execute(sql, (self.id,))

        dbRecord: dict = cursor.fetchone()
        
        db.close()

        if not dbRecord:    # record not found
            return False

        self.payment_id   = dbRecord.get('payment_id', None)
        self.session_id   = dbRecord.get('session_id', None)
        self.responded_on = dbRecord.get('responded_on', None)
        self.created_on   = dbRecord.get('created_on', None)
        self.status       = RequestStatus.getStatus(dbRecord.get('status', RequestStatus.pending))

        return True

    #-----------------------------------------------------
    # Update the status of a request
    #
    # Returns an int: 
    #   the number of rows affected by the update 
    #   or -1 if there was an error
    # ----------------------------------------------------
    def updateStatus(self) -> int:
        if not self.id:
            return -1
        
        db = DB()
        db.connect()
        cursor = db.getCursor(False)

        sql = '''
        UPDATE  Product_Requests 
        SET     status = %s,
                responded_on = NOW()
        WHERE   id = %s
        '''

        parms = (self.status.value, self.id)
        
        row_count = -1

        try:
            cursor.execute(sql, parms)
            db.commit()
            row_count = cursor.rowcount
        except Exception as e:
            print(e)
        finally:
            db.close()

        return row_count









