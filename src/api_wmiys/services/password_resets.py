"""
**********************************************************************************************

Business logic for password resets.

**********************************************************************************************
"""
from __future__ import annotations

import flask

from api_wmiys.domain import models
from api_wmiys.repository import password_resets as password_resets_repo


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
def responses_POST() -> flask.Response:
    return 'password reset: POST'


#----------------------------------------------------------
# Update an existing password reset record
#----------------------------------------------------------
def responses_PUT() -> flask.Response:
    return 'password reset: PUT'



