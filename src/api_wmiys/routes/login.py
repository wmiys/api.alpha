"""
Package:        login
Url Prefix:     /login
Description:    Handles all the routing for loggin in.
"""

import flask
from http import HTTPStatus
from ..common import security
from ..models import User


login = flask.Blueprint('login', __name__)


#----------------------------------------------------------
# Login a client
#----------------------------------------------------------
@login.route('', methods=['GET'])
def loginRoute():

    email = flask.request.args.get('email', None)
    password = flask.request.args.get('password', None)
    
    if None in [email, password]:
        return ('Missing required field.', HTTPStatus.BAD_REQUEST.value)

    user_id = security.getUserID(email, password)

    # make sure the user is authorized
    if not user_id:
        return ('', HTTPStatus.NOT_FOUND.value)

    user = User(id=user_id)
    user.fetch()
    return flask.jsonify(user.as_dict(False))