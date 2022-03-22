"""
Package:        locations
Url Prefix:     /locations/
Description:    Routing for locations
"""

import flask
from ..common import security
from api_wmiys.services import locations as location_services

bp_locations = flask.Blueprint('locationsBP', __name__)


#----------------------------------------------------------
# Get a single location
#----------------------------------------------------------
@bp_locations.get('<int:location_id>')
@security.login_required
def getLocations(location_id: int):
    return location_services.response_GET(location_id)
