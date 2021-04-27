import flask
from flask import Blueprint, jsonify, request
import api_wmiys.Security as Security
from api_wmiys.Security import requestGlobals
from api_wmiys.login.Login import Login
from api_wmiys.users.User import User


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