
from ..models import login
from .globals import Globals
import flask
from flask import request
from functools import wraps, update_wrapper
from ..db import DB

# setup the global variables container
requestGlobals = Globals(client_id=None)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not request.authorization:
            flask.abort(401)
        
        # make sure the user is authorized
        clientID = login.getUserID(request.authorization.username, request.authorization.password)
        if clientID == None:
            flask.abort(401)
        
        global requestGlobals
        requestGlobals.client_id = clientID

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap


#------------------------------------------------------
# Get a user's id from their email/password combination
#
# Parms:
#   email - user's email
#   password - user's password
# 
# Returns: 
#   user's id - (email/password combo was correct)
#   None - (INCORRECT email/password combo)
#------------------------------------------------------
def getUserID(email: str, password: str):
    db = DB()
    db.connect()

    cursor = db.getCursor(True)

    sql = 'SELECT u.id as id FROM Users u WHERE u.email = %s AND u.password = %s'
    parms = (email, password)

    try:
        cursor.execute(sql, parms)
        record_set: dict = cursor.fetchone()
        result = record_set.get('id', None)
    except:
        result = None
    finally:
        db.close()

    return result   