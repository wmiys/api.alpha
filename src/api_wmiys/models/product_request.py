from __future__ import annotations
from ..db import DB


#-----------------------------------------------------
# Retrieve all the requests that a lender has received.
# 
# Parms:
#   lender_id - the lender's user_id
# ----------------------------------------------------
def getReceived(lender_id) -> list[dict]:
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    sql = '''
        SELECT * 
        FROM View_Requests_Lender v 
        WHERE v.product_id IN (
            SELECT id FROM Products p WHERE p.user_id = %s
        )
    '''

    parms = (lender_id,)
    cursor.execute(sql, parms)
    requests = cursor.fetchall()
    db.close()

    return requests





class ProductRequest:

    #-----------------------------------------------------
    # Constructor
    # ----------------------------------------------------
    def __init__(self, id=None, payment_id=None, session_id=None, status=None, responded_on=None, created_on=None):
        self.id           = id
        self.payment_id   = payment_id
        self.session_id   = session_id
        self.status       = status
        self.responded_on = responded_on
        self.created_on   = created_on

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
    # ----------------------------------------------------
    def insert(self):
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








