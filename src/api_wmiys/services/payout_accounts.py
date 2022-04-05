"""
**********************************************************************************************
Payout Accounts represent the lender's connected account on stripe. 

Before users can start lending their products, they need to setup an account with stripe.

This is so we can pay out their account balance to their bank account after successfully 
lending out their products. 
**********************************************************************************************
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from uuid import UUID
import flask
from wmiys_common import utilities
from api_wmiys.repository import payout_accounts as repo
from api_wmiys.common import responses
from api_wmiys.common import serializers
from api_wmiys.domain import models
from api_wmiys import payments

class SqlBool(Enum):
    FALSE = 0
    TRUE = 1

#------------------------------------------------------
# RESPONSE: create a new payout account
#------------------------------------------------------
def response_POST() -> flask.Response:
    # setup a new PayoutAccount domain model
    account_new = setupNewPayoutAccount()

    # send it to the repo to insert into the database
    db_result = repo.insert(account_new)

    if not db_result.successful:
        return responses.badRequest(str(db_result.error))

    return _standardResponse(account_new, responses.created)

#------------------------------------------------------
# Create a new PayoutAccount model with a new stripe id
#------------------------------------------------------
def setupNewPayoutAccount() -> models.PayoutAccount:
    
    # register a new customer account with stripe
    # we need to do this because we need to save the stripe_id value in our database    
    new_stripe_account = payments.createNewStripeAccount(flask.g.client_id)

    # now, setup a new PayoutAccount model object to pass to the repository
    account = models.PayoutAccount(
        id         = utilities.getUUID(False),
        user_id    = flask.g.client_id,
        account_id = new_stripe_account.stripe_id,
        created_on = datetime.now()
    )
    
    return account

#------------------------------------------------------
# RESPONSE: update an existing payout account
#------------------------------------------------------
def response_PUT(payout_account_id: UUID) -> flask.Response:
    # build a PayoutAccount domain model to send to the repository for update
    account = extractFormData()
    account.id = payout_account_id
    account.user_id = flask.g.client_id

    # update the database info
    db_result = repo.update(account)

    if not db_result.successful:
        return responses.badRequest(str(db_result.error))

    # return the updated PayoutAccount data
    return _standardResponse(account, responses.updated)

#------------------------------------------------------
# Extract/serialize the request's form data into a PayoutAccount object
#------------------------------------------------------
def extractFormData() -> models.PayoutAccount:
    form = flask.request.form.to_dict()
    serializer = serializers.PayoutAccountSerializer(form)
    serialized_model = serializer.serialize().model
    
    return serialized_model


#------------------------------------------------------
# RESPONSE: get single payout account
#------------------------------------------------------
def response_GET(payout_account_id: UUID) -> flask.Response:
    account = models.PayoutAccount(
        id      = payout_account_id,
        user_id = flask.g.client_id,
    )

    return _standardResponse(account, responses.get)


#------------------------------------------------------
# The standardized response routine for single payout accounts
#
# Args:
# - payout_account: the payout account to return (must have id and user_id field values)
# - responses_callback: api_wmiys.common.responses callback routine
#------------------------------------------------------
def _standardResponse(payout_account: models.PayoutAccount, responses_callback) -> flask.Response:
    account = getView(payout_account.id, payout_account.user_id)

    if not account:
        return responses.notFound()
    
    _transformAccountConfirmedValue(account)

    return responses_callback(account)

#------------------------------------------------------
# Get a payout account view dict
#------------------------------------------------------
def getView(payout_account_id: UUID, user_id: int) -> dict | None:
    account = models.PayoutAccount(
        id      = payout_account_id,
        user_id = user_id
    )

    db_result = repo.select(account)

    return db_result.data


#------------------------------------------------------
# RESPONSE: get all
#------------------------------------------------------
def response_GET_ALL() -> flask.Response:
    db_result = repo.selectAll(flask.g.client_id)

    if not db_result.successful:
        responses.badRequest(str(db_result.error))

    accounts = db_result.data or []

    # transform all sql bool types into python bools
    for account in accounts:
        _transformAccountConfirmedValue(account)
    
    return responses.get(accounts)

#------------------------------------------------------
# Parse the payout account's confirm db field value into a python boolean
#------------------------------------------------------
def _transformAccountConfirmedValue(payout_account_record: dict):
    confirmed_valued = payout_account_record.get('confirmed') or SqlBool.FALSE
    payout_account_record['confirmed'] = sqlBoolToPython(confirmed_valued)


#------------------------------------------------------
# Get the boolean representation of the given SqlBool value
#------------------------------------------------------
def sqlBoolToPython(value: SqlBool) -> bool:
    if value == SqlBool.FALSE:
        return False
    else:
        return True




