"""
**********************************************************************************************
Product requests are what the name implies... a renter has found a listing that is available
during the given start/end range, the renter has successfully paid for the product rental with stripe
and we have collected the funds. Now, the lender needs to finally approve the product rental with 
the renter.

Initially, a request status is set to 'pending'. The lender has 24 hours to respond to the 
request before being marked as 'expired' and the renter is fully refunded (and the request
cannot be responded to). Lenders can respond to a requests by either accepting or denying them.

Once a request status is either responded to or it expires, lenders cannot update a request.
**********************************************************************************************
"""


from __future__ import annotations
import flask
from api_wmiys.domain import models


