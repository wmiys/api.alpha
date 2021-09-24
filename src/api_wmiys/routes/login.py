"""
Package:        login
Url Prefix:     /login
Description:    Handles all the routing for loggin in.
"""

import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from ..models import Login, User


login = Blueprint('login', __name__)


@login.route('', methods=['GET'])
def loginRoute():
    userID = Login.getUserID(request.args['email'], request.args['password'])

    # make sure the user is authorized
    if userID == None:
        flask.abort(404)

    user = User(id=userID)
    user.fetch()
    return jsonify(user.as_dict(False))