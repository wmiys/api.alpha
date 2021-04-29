DELIMITER $$
CREATE DEFINER=`rrickgau_main`@`24.13.68.79` FUNCTION `Is_Product_Available`(
    in_product_id INT UNSIGNED,
    in_starts_on DATE,
    in_ends_on DATE
) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    
    -- This function checks if a product has any existing product availability records that fall into the date range passed in
    DECLARE num_records  INT;
    DECLARE result BOOL;
    
    SELECT COUNT(*) 
    INTO num_records
    FROM Product_Availability pa
    WHERE 
        (
            -- ensure the input dates don't conflict with any product availability records
            (in_starts_on >= pa.starts_on AND in_starts_on <= pa.ends_on) OR    -- requested starts on does not fall into a Product_Availability record
            (in_ends_on >= pa.starts_on AND in_ends_on <= pa.ends_on)           -- requested ends on does not fall into a Product_Availability record
        ) 
        AND pa.product_id = in_product_id;
    
    IF num_records > 0 THEN     -- no conflicting dates
        SET result = FALSE;
    ELSE 
        SET result = TRUE;
    END IF;
    
    RETURN (result);
    
END$$
DELIMITER ;
