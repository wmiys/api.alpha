DELIMITER $$
CREATE PROCEDURE `Search_Products_Setup`(
    IN in_dropoff_location_id INT UNSIGNED, 
    IN in_starts_on DATE,
    IN in_ends_on DATE
)
BEGIN
    
    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_products_available (
		product_id INT UNSIGNED
	);
    
    DELETE FROM tmp_products_available;
    
    INSERT INTO tmp_products_available (product_id)
    SELECT p.id
	FROM Products p
    WHERE 
        IS_PRODUCT_AVAILABLE(p.id, in_starts_on, in_ends_on) = TRUE                         -- date ranges don't conflict with any existing product availability records
        AND  MILES_BETWEEN(p.location_id, in_dropoff_location_id) <= p.dropoff_distance;    -- product dropoff distance must be within distance between the renter and the lender
        AND Product_Has_Conflicting_Requests(p.id, in_starts_on, in_ends_on) = FALSE;		-- product does not have any conflicting product_requests during the given range
END$$
DELIMITER ;
