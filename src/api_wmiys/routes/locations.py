"""
Package:        locations
Url Prefix:     /locations/
Description:    Routing for locations
"""

import flask
from ..common import security
from ..models import Location

locationsBP = flask.Blueprint('locationsBP', __name__)


#----------------------------------------------------------
# Get a single location
#----------------------------------------------------------
@locationsBP.route('<int:location_id>', methods=['GET'])
@security.login_required
def getLocations(location_id: int):
    location = Location(location_id)
    location.load()

    return flask.jsonify(location.toDict())
