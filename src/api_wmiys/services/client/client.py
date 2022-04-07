"""
**********************************************************************************************

Services to gather all the client's data

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass

from pymysql.connection import ConnectionDict
from pymysql.structs import DbOperationResult
from api_wmiys.domain import models
from api_wmiys.common import serializers
from .serializer import ClientRecordSetSerializer
from api_wmiys.domain.internal.client import RecordSetIndex
from api_wmiys.domain.internal.client import ClientRecordSetCollection
from api_wmiys.domain.internal.client import Client



def getClientModel(user_id) -> Client:
    records_collection = getRecordSetCollection(user_id)

    serializer = ClientRecordSetSerializer(records_collection)

    client = serializer.serialize()

    return client


#------------------------------------------------------
# Transform the record set list into a RecordSetCollection
#------------------------------------------------------
def getRecordSetCollection(user_id) -> ClientRecordSetCollection:
    db_result = callStoredProcedure(user_id)

    record_sets = db_result.data
    
    record_set_collection = ClientRecordSetCollection(
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