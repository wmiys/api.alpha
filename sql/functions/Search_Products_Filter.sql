DELIMITER $$
CREATE FUNCTION `Search_Products_Filter`(
    in_product_id INT UNSIGNED,
    in_dropoff_location_id INT UNSIGNED,
    in_starts_on DATE,
    in_ends_on DATE
) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    DECLARE product_dropoff_distance SMALLINT UNSIGNED;
    DECLARE product_location_id INT UNSIGNED;
    
    SELECT p.dropoff_distance, p.location_id 
    INTO product_dropoff_distance, product_location_id
    FROM Products p
    WHERE p.id = in_product_id;
    
    -- date ranges don't conflict with any existing product availability records
    IF IS_PRODUCT_AVAILABLE(in_product_id, in_starts_on, in_ends_on) != TRUE THEN
        RETURN (FALSE);
    END IF;
    
    -- product dropoff distance must be within distance between the renter and the lender
     IF MILES_BETWEEN(product_location_id, in_dropoff_location_id) > product_dropoff_distance THEN
         RETURN (FALSE);
     END IF;
 
 RETURN (TRUE);
 
END$$
DELIMITER ;
