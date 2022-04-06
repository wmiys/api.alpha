"""
Package:        test
Url Prefix:     /test
Description:    Test endpoint
"""
from __future__ import annotations
from dataclasses import dataclass
import flask
from api_wmiys.common import security
from pymysql.connection import ConnectionBase, ConnectionDict
from pymysql.structs import DbOperationResult

from api_wmiys.common import responses


bp_test = flask.Blueprint('bp_test', __name__)

#------------------------------------------------------
# Test endpoint
#------------------------------------------------------
@bp_test.route('')
# @security.no_external_requests
@security.login_required
def test():

    result = getData()

    return responses.get(result)



class RecordSetIndex:
    PRODUCTS                   = 0
    PRODUCT_AVAILABILITY       = 1
    PRODUCT_IMAGES             = 2
    PRODUCT_REQUESTS_RECEIVED  = 3
    PRODUCT_REQUESTS_SUBMITTED = 4
    BALANCE_TRANSFERS          = 5
    PAYOUT_ACCOUNTS            = 6


@dataclass
class RecordSetCollection:
    products                   : list[dict] = None
    product_availability       : list[dict] = None
    product_images             : list[dict] = None
    product_requests_received  : list[dict] = None
    product_requests_submitted : list[dict] = None
    balance_transfers          : list[dict] = None
    payout_accounts            : list[dict] = None

def getData():

    records_collection = getRecordSetCollection(flask.g.client_id)

    return records_collection


#------------------------------------------------------
# Transform the record set list into a RecordSetCollection
#------------------------------------------------------
def getRecordSetCollection(user_id) -> RecordSetCollection:

    db_result = callStoredProcedure(user_id)

    record_sets = db_result.data
    
    record_set_collection = RecordSetCollection(
        products                   = record_sets[RecordSetIndex.PRODUCTS].fetchall(),
        product_availability       = record_sets[RecordSetIndex.PRODUCT_AVAILABILITY].fetchall(),
        product_images             = record_sets[RecordSetIndex.PRODUCT_IMAGES].fetchall(),
        product_requests_received  = record_sets[RecordSetIndex.PRODUCT_REQUESTS_RECEIVED].fetchall(),
        product_requests_submitted = record_sets[RecordSetIndex.PRODUCT_REQUESTS_SUBMITTED].fetchall(),
        balance_transfers          = record_sets[RecordSetIndex.BALANCE_TRANSFERS].fetchall(),
        payout_accounts            = record_sets[RecordSetIndex.PAYOUT_ACCOUNTS].fetchall(),
    )

    return record_set_collection
    

#------------------------------------------------------
# Fetch the result sets from the database stored procedure
#------------------------------------------------------
def callStoredProcedure(user_id) -> DbOperationResult:
    result =  DbOperationResult(successful=True)
    
    db = ConnectionDict()
    parms = [user_id,]

    try:
        db.connect()
        mycursor = db.getCursor()
        
        mycursor.callproc('Get_User_Data', parms)
        result.data = list(mycursor.stored_results())

    except Exception as e:
        result.successful = False
        result.error = e
        result.data = None
    
    finally:
        db.close()

    return result