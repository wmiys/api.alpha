"""
**********************************************************************************************
A product availability record represents a lender provided date range that they do not wish for
their product to be available for rent. 

So renters will not be able to see the product in the search results if their start/end date range
conflicts with any product availability record.

Furthermore, products that have conflicting availability records will not be able to even receive 
requests from renters if the starts/ends range conflicts.
**********************************************************************************************
"""
from __future__ import annotations
import flask
from wmiys_common import utilities
from api_wmiys.repository import product_availability as product_availability_repo
from api_wmiys.common import responses


#----------------------------------------------------------
# Respond to a GET ALL request
#----------------------------------------------------------
def responses_GET_ALL(product_id) -> flask.Response:
    result = product_availability_repo.selectAll(product_id)

    if not result.successful:
        return responses.badRequest(str(result.error))

    return responses.get(result.data)


#----------------------------------------------------------
# Respond to a POST request
#----------------------------------------------------------
def responses_POST() -> flask.Response:
    pass


#----------------------------------------------------------
# Respond to a GET request
#----------------------------------------------------------
def responses_GET() -> flask.Response:
    pass


#----------------------------------------------------------
# Respond to a PUT request
#----------------------------------------------------------
def responses_PUT() -> flask.Response:
    pass


#----------------------------------------------------------
# Respond to a DELETE request
#----------------------------------------------------------
def responses_DELETE() -> flask.Response:
    pass





