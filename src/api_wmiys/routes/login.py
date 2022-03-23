"""
Package:        login
Url Prefix:     /login
Description:    Handles all the routing for loggin in.
"""

from http import HTTPStatus

import flask

from api_wmiys.common import security
from api_wmiys.services import users as user_services


# module blueprint
bp_login = flask.Blueprint('login', __name__)


#----------------------------------------------------------
# Login a client
#----------------------------------------------------------
@bp_login.get('')
def loginRoute():
    email    = flask.request.args.get('email', None)
    password = flask.request.args.get('password', None)
    
    if None in [email, password]:
        return ('Missing required field.', HTTPStatus.BAD_REQUEST.value)

    user_id = security.getUserID(email, password)

    # make sure the user is authorized
    if not user_id:
        return ('', HTTPStatus.NOT_FOUND.value)


    # return the user data to the client
    user_output_view = user_services.getUserView(user_id)
    
    return flask.jsonify(user_output_view)
