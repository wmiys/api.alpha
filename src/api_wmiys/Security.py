
from api_wmiys.login.Login import Login
from api_wmiys.Globals import Globals
import flask
from flask import request
from functools import wraps, update_wrapper

# setup the global variables container
requestGlobals = Globals(client_id=None)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not request.authorization:
            flask.abort(401)
        
        # make sure the user is authorized
        clientID = Login.getUserID(request.authorization.username, request.authorization.password)
        if clientID == None:
            flask.abort(401)
        
        global requestGlobals
        requestGlobals.client_id = clientID

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap
