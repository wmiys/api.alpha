#************************************************************************************
#
# This class handles all the business logic for the users resource.
#
#************************************************************************************


from __future__ import annotations
from enum import Enum

import flask
from prettytable import DOUBLE_BORDER
from pymysql.structs import DbOperationResult

from api_wmiys.repository import users as users_repo
from api_wmiys.domain import models
from api_wmiys.common import responses
from api_wmiys.common import serializers

SQL_ERROR_DUPLICATE_KEY = 1062

#------------------------------------------------------
# Bad request error messages returned in the response
#------------------------------------------------------
class BadResponseErrorMessages(str, Enum):
    MISSING_REQUIRED_FIELD = 'Missing one or more required fields.'
    EMAIL_IN_USE           = 'The email is already in use'


#------------------------------------------------------
# Retrieve a single user
#------------------------------------------------------
def response_GET(user_id) -> flask.Response:
    # make sure the user is authorized
    if flask.g.client_id != user_id:
        return responses.notFound()

    # fetch the user from the database
    user_dict = getUserView(user_id)

    if not user_id:
        return responses.notFound()

    return responses.get(user_dict)


#------------------------------------------------------
# Update an existing user
#------------------------------------------------------
def response_PUT(user_id) -> flask.Response:
    # make sure the user is authorized
    if flask.g.client_id != user_id:
        return responses.notFound()

    user_model = generateUpdatedUserModelFromForm(user_id)

    # send the model to the repository to record the changes in the database
    result = users_repo.update(user_model)

    if not result.successful:
        return _handleDbError(result)


    return _standardResponseWithView(user_id, responses.updated)

#------------------------------------------------------
# Create a new user
#------------------------------------------------------
def response_POST() -> flask.Response:
    new_user = extractUserModelFromForm()

    # verify that all the required fields are set
    if not areRequiredAttributesSet(new_user):
        return responses.badRequest(BadResponseErrorMessages.MISSING_REQUIRED_FIELD)
    
    # attempt to insert the user into the database
    db_result = users_repo.insert(new_user)

    # if the sql command was not successful, handle it accordingly
    if not db_result.successful:
        return _handleDbError(db_result)
    
    # a successful database insert command returns the new user's id
    new_user_id = db_result.data

    # now, call the standardized single user return routine for the new user
    return _standardResponseWithView(new_user_id, responses.created)

#------------------------------------------------------
# Verifies that all the required fields of the given User object are set (not null)
# All these fields need to have a value before inserting the object into the database
#
# Returns a bool
#   - true: all the required attributes are set and are not null
#   - false: one or more of the attributes is null
#------------------------------------------------------
def areRequiredAttributesSet(user: models.User) -> bool:
    required_user_fields = [
        user.email, 
        user.password, 
        user.name_first, 
        user.name_last, 
        user.birth_date
    ]

    if None in required_user_fields:
        return False
    else:
        return True


#------------------------------------------------------
# Serialize the incoming request form data into a User domain model
#------------------------------------------------------
def extractUserModelFromForm() -> models.User:
    form = flask.request.form.to_dict()
    serializer = serializers.UserSerializer(form)
    user_model: models.User = serializer.serialize().model

    return user_model

#------------------------------------------------------
# Load up an User model with all the current values stored in the database
# Then using the incoming request form data, move those values into the model
#------------------------------------------------------
def generateUpdatedUserModelFromForm(user_id) -> models.User:
    # load up a User domain model with all the existing data in its attributes
    user_model_existing = getUserModel(user_id)

    # serialize the incoming request form data into a User domain model
    form = flask.request.form.to_dict()
    serializer = serializers.UserSerializer(form, user_model_existing)
    user_model: models.User = serializer.serialize().model
    
    # explicitly set a few of the model's attribute values
    user_model.id = user_id
    user_model.password = flask.g.client_password

    return user_model


#------------------------------------------------------
# Get the user domain model
#------------------------------------------------------
def getUserModel(user_id) -> models.User:
    user_view = getUserView(user_id)
    user_model = _serializeView(user_view)
    user_model.id = user_id

    return user_model

#------------------------------------------------------
# Get the user view dict from the database
#------------------------------------------------------
def getUserView(user_id) -> dict | None:
    user_model = models.User(id=user_id)
    result = users_repo.select(user_model)

    return result.data
    


#------------------------------------------------------
# Standard response for returning a single User record
#
# Args:
#   - user_id: the user id
#   - responses_callback: api_wmiys.common.responses callback to generate the appropriate flask response with headers
#------------------------------------------------------
def _standardResponseWithView(user_id, responses_callback) -> flask.Response:
    output = getUserView(user_id)
    
    if not output:
        return responses.notFound()

    return responses_callback(output)


#------------------------------------------------------
# handle some of the database errors
#------------------------------------------------------
def _handleDbError(db_result: DbOperationResult) -> flask.Response:
    if db_result.error.errno == SQL_ERROR_DUPLICATE_KEY:
        return responses.badRequest(BadResponseErrorMessages.EMAIL_IN_USE)

    return responses.badRequest(str(db_result.error))

#------------------------------------------------------
# Get a user by their email/password combination
#------------------------------------------------------
def getUserByEmailAndPassword(email, password) -> models.User | None:
    db_result = users_repo.selectByEmailAndPassword(email, password)

    if not db_result.successful:
        raise db_result.error

    if not db_result.data:
        return None
    
    return _serializeView(db_result.data)


#------------------------------------------------------
# Serialize the given user view into a User domain model
#------------------------------------------------------
def _serializeView(user_view: dict) -> models.User:
    serializer = serializers.UserSerializer(user_view)
    user_model = serializer.serialize().model

    return user_model

