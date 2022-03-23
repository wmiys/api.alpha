

import flask

from api_wmiys.repository import users as users_repo
from api_wmiys.domain import models
from api_wmiys import common


#------------------------------------------------------
# Retrieve a single user
#------------------------------------------------------
def response_GET(user_id) -> flask.Response:
    # make sure the user is authorized
    if flask.g.client_id != user_id:
        return common.responses.notFound()

    # fetch the user from the database
    user_dict = getUserView(user_id)

    if not user_id:
        return common.responses.notFound()

    return common.responses.get(user_dict)

#------------------------------------------------------
# Get the user view dict
#------------------------------------------------------
def getUserView(user_id) -> dict:
    user_model = models.User(
        id = user_id
    )

    result = users_repo.select(user_model)

    return result.data


#------------------------------------------------------
# Update an existing user
#------------------------------------------------------
def response_PUT(user_id) -> flask.Response:

    



    return 'update user'


