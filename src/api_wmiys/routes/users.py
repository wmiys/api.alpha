"""
Module:        users
Url Prefix:     /users
"""

from __future__ import annotations

import flask

from api_wmiys.common import security
from api_wmiys.services import users as user_services

bp_users = flask.Blueprint('routeUser', __name__)

#------------------------------------------------------
# Create new user
#------------------------------------------------------
@bp_users.post('')
def usersPost():
    return user_services.response_POST()

#------------------------------------------------------
# Get a single user or update an existing user
#------------------------------------------------------
@bp_users.route('<int:user_id>', methods=['GET', 'PUT'])
@security.login_required
def userGetPost(user_id):
    if flask.request.method == 'PUT':
        return user_services.response_PUT(user_id)    
    else:
        return user_services.response_GET(user_id)