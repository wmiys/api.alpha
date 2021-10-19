DELIMITER $$
CREATE FUNCTION Product_Has_Conflicting_Requests (
	in_product_id INT,
    in_starts_on DATE,
    in_ends_on DATE
) 
RETURNS BOOL DETERMINISTIC
BEGIN
    
    -- This function checks if the given product has any existing product requests within the given range
    -- If returns false - product has no conflicting requests
    -- If return true - product does have a conflicting request
    
    DECLARE result BOOL;
    DECLARE num_records INT;
    
    SELECT COUNT(*) 
    INTO num_records 
    FROM Product_Requests pr
    INNER JOIN Payments pay ON 
        pay.id = pr.payment_id AND
        pay.product_id = in_product_id AND
        RANGES_CONFLICT(in_starts_on, in_ends_on, pay.starts_on, pay.ends_on) = TRUE
    WHERE pr.status IN ('accepted', 'pending');
    
    -- needs to be a count of 0 for the product to have no conflicting product requests
    IF num_records = 0 THEN
        SET result = FALSE;
    ELSE
        SET result = TRUE;
    END IF;
    
    RETURN (result);
    
END$$
DELIMITER ;