DELIMITER $$
CREATE PROCEDURE `Search_Products`(
	IN in_dropoff_location_id INT UNSIGNED, 
    IN in_product_categories_sub_id INT UNSIGNED,
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
		p.product_categories_sub_id = in_product_categories_sub_id                          -- same product categories sub as the request
        AND IS_PRODUCT_AVAILABLE(p.id, in_starts_on, in_ends_on) = TRUE                     -- date ranges don't conflict with any existing product availability records
        AND  MILES_BETWEEN(p.location_id, in_dropoff_location_id) <= p.dropoff_distance;    -- product dropoff distance must be within distance between the renter and the lender
        
    SELECT * FROM View_Products vp
    WHERE vp.id IN (SELECT * FROM tmp_products_available);
	
    DROP TEMPORARY TABLE tmp_products_available;

END$$
DELIMITER ;
