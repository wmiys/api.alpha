
-- This event sets all expired product request status' to 'expired'
-- requests are considered expired when they have a status of 'pending' and it's been 24 hours since it was created.

CREATE EVENT Event_Update_Expired_Product_Requests
ON SCHEDULE EVERY 1 HOUR
STARTS CURRENT_TIMESTAMP
ENDS CURRENT_TIMESTAMP + INTERVAL 10 YEAR
DO
    UPDATE Product_Requests 
    SET 
        status = 'expired'
    WHERE
        status = 'pending'
        AND CURRENT_TIMESTAMP() > DATE_ADD(created_on, INTERVAL 24 HOUR);