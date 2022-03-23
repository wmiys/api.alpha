from __future__ import annotations

import flask

from api_wmiys.repository import users as users_repo
from api_wmiys.domain import models
from api_wmiys.common import responses
from api_wmiys.common import serializers
from pymysql.structs import DbOperationResult


SQL_ERROR_DUPLICATE_KEY = 1062

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

    output = getUserView(user_id)
    
    if not output:
        return responses.notFound()

    return responses.updated(output)

#------------------------------------------------------
# handle some of the database errors
#------------------------------------------------------
def _handleDbError(db_result: DbOperationResult) -> flask.Response:

    if db_result.error.errno == SQL_ERROR_DUPLICATE_KEY:
        return responses.badRequest('The email is already in use')

    return responses.badRequest(str(db_result.error))

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
    serializer = serializers.UserSerializer(user_view)
    user_model: models.User = serializer.serialize().model

    user_model.id = user_id

    return user_model


#------------------------------------------------------
# Get the user view dict
#------------------------------------------------------
def getUserView(user_id) -> dict | None:
    user_model = models.User(
        id = user_id
    )

    result = users_repo.select(user_model)

    return result.data