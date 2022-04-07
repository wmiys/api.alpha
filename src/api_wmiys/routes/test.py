"""
**********************************************************************************************
Package:        test
Url Prefix:     /test
Description:    Test endpoint
**********************************************************************************************
"""
from __future__ import annotations

import flask

from api_wmiys.common import security
from api_wmiys.common import responses
from api_wmiys.services.client import client as client_services
from wmiys_common.utilities import dumpJson

bp_test = flask.Blueprint('bp_test', __name__)

#------------------------------------------------------ 
# Fetch all the records (no serializing)
#------------------------------------------------------
@bp_test.route('')
@security.login_required
def test():
    client_model = client_services.getClientModel(flask.g.client_id)
    dumpJson(client_model)

    return responses.get(client_model)


#------------------------------------------------------
# Fetch all the records (no serializing)
#------------------------------------------------------
@bp_test.route('no-serialization')
@security.login_required
def no_serialization():
    result = client_services.getRecordSetCollection(flask.g.client_id)
    return responses.get(result)



