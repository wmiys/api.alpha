DELIMITER $$
CREATE PROCEDURE `Search_Products`(
	IN in_dropoff_location_id INT UNSIGNED, 
    IN in_starts_on DATE,
    IN in_ends_on DATE
)
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_products_available (
		product_id INT UNSIGNED
	);
    
    DELETE FROM tmp_products_available;
	
    Call Search_Products_Setup(in_dropoff_location_id, in_starts_on, in_ends_on);

	SELECT * FROM View_Search_Products vp
	WHERE vp.id IN (SELECT * FROM tmp_products_available);
	
    DROP TEMPORARY TABLE tmp_products_available;
END$$
DELIMITER ;
