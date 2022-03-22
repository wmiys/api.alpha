"""
**********************************************************************************************

Location services

**********************************************************************************************
"""


from __future__ import annotations

import flask

from api_wmiys.repository import locations as locations_repo
from api_wmiys.domain import models
from api_wmiys import common

#------------------------------------------------------
# Respond to a GET request
#------------------------------------------------------
def response_GET(location_id: int) -> flask.Response:
    location_model = models.Location(
        id = location_id
    )

    result = locations_repo.select(location_model)
    
    # make sure sql command was successful and the location exists
    if not result.successful:
        return common.responses.badRequest(str(result.error))
    elif not result.data:
        return common.responses.notFound()

    # all good - return the location
    return common.responses.get(result.data)



