"""
Package:        login
Url Prefix:     /login
Description:    Handles all the routing for loggin in.
"""

import flask
from ..common import security
from ..models import User


login = flask.Blueprint('login', __name__)


#----------------------------------------------------------
# Login a client
#----------------------------------------------------------
@login.route('', methods=['GET'])
def loginRoute():
    userID = security.getUserID(flask.request.args['email'], flask.request.args['password'])

    # make sure the user is authorized
    if userID == None:
        flask.abort(404)

    user = User(id=userID)
    user.fetch()
    return flask.jsonify(user.as_dict(False))