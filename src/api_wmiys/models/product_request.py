from __future__ import annotations
from enum import Enum
from uuid import UUID
from ..db import DB
from ..common import user_image


# database table views
SQL_VIEW_LENDER = 'View_Requests_Lender'
SQL_VIEW_RENTER = 'View_Requests_Renter'


#-----------------------------------------------------
# Possible product request status values
# ----------------------------------------------------
class RequestStatus(str, Enum):
    pending  = 'pending'
    accepted = 'accepted'
    denied   = 'denied'
    expired  = 'expired'


#-----------------------------------------------------
# Product Request class
# ----------------------------------------------------
class ProductRequest:

    #-----------------------------------------------------
    # Constructor
    # ----------------------------------------------------
    def __init__(self, id: UUID=None, payment_id=None, session_id=None, status=RequestStatus.pending, responded_on=None, created_on=None):
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
        return self._getBase(SQL_VIEW_LENDER)

    def getRenter(self) -> dict:        
        return self._getBase(SQL_VIEW_RENTER)

    def _getBase(self, sql_table_source: str) -> dict:
        if not self.id:
            return None
        
        db = DB()
        db.connect()
        cursor = db.getCursor(True)

        sql = f'SELECT * FROM {sql_table_source} v WHERE v.id = %s'
        parms = (str(self.id),)

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
        if None in [self.id, self.payment_id, self.session_id]:
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

        sql = 'INSERT INTO Product_Requests (id, payment_id, session_id) VALUES (%s, %s, %s)'
        parms = (str(self.id), self.payment_id, self.session_id)

        try:
            cursor.execute(sql, parms)
            db.commit()
            successful = True
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
        cursor.execute(sql, (str(self.id),))

        dbRecord: dict = cursor.fetchone()
        
        db.close()

        if not dbRecord:    # record not found
            return False

        self.payment_id   = dbRecord.get('payment_id', None)
        self.session_id   = dbRecord.get('session_id', None)
        self.responded_on = dbRecord.get('responded_on', None)
        self.created_on   = dbRecord.get('created_on', None)
        self.status       = RequestStatus(dbRecord.get('status'))

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

        parms = (self.status.value, str(self.id))
        
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


#-----------------------------------------------------
# Retrieve all the requests that a lender has received.
# 
# Parms:
#   lender_id - the lender's user_id
# ----------------------------------------------------
def getReceivedAll(lender_id) -> list[dict]:
    sql = f'''
    SELECT * FROM {SQL_VIEW_LENDER} v 
    WHERE v.product_id IN (SELECT id FROM Products p WHERE p.user_id = %s)
    ORDER BY v.created_on DESC
    '''

    parms = (lender_id,)

    return _getRequestsBase(sql, parms)


#-----------------------------------------------------
# Retrieve all the requests that a lender has received
# that have the specified status.
# 
# Parms:
#   lender_id: the lender's user_id
#   status: the status to filter by
# ----------------------------------------------------
def getReceivedFilterByStatus(lender_id, status: RequestStatus) -> list[dict]:
    sql = f'''
    SELECT  * FROM {SQL_VIEW_LENDER} v 
    WHERE   v.product_id IN (SELECT id FROM Products p WHERE p.user_id = %s) 
            AND v.status = %s
    ORDER BY v.created_on DESC
    '''

    parms = (lender_id, status.value)

    return _getRequestsBase(sql, parms)

#-----------------------------------------------------
# Retrieve all the requests that a renter has submitted.
# 
# Parms:
#   renter_id: the renter's user id
# ----------------------------------------------------
def getSubmitted(renter_id) -> list[dict]:
    sql = f'SELECT * FROM {SQL_VIEW_RENTER} v WHERE v.renter_id = %s ORDER BY v.created_on DESC'
    parms = (renter_id,)

    db_result = _getRequestsBase(sql, parms)

    image_prefix = user_image.getCoverUrl()

    for record in db_result:
        if record.get('product_image'):
            record['product_image'] = image_prefix + record['product_image']

    return db_result

#-----------------------------------------------------
# Retrieve all the requests that a renter has submitted
# that have the specified status.
# 
# Parms:
#   renter_id: the renter's user_id
#   status: the status to filter by
# ----------------------------------------------------
def getSubmittedFilterByStatus(renter_id: int, status: RequestStatus) -> list[dict]:
    sql = f'''
    SELECT * FROM {SQL_VIEW_RENTER} v 
    WHERE v.renter_id = %s AND v.status = %s
    ORDER BY v.created_on DESC
    '''
    parms = (renter_id, status.value)
    
    db_result = _getRequestsBase(sql, parms)

    image_prefix = user_image.getCoverUrl()

    for record in db_result:
        if record.get('product_image'):
            record['product_image'] = image_prefix + record['product_image']

    return db_result


#-----------------------------------------------------
# Base template function for getting requests
# 
# Parms:
#   sql: sql to execute
#   parms: the parms to submit
# ----------------------------------------------------
def _getRequestsBase(sql: str, parms: tuple):
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    cursor.execute(sql, parms)
    requests = cursor.fetchall()
    
    db.close()

    return requests






