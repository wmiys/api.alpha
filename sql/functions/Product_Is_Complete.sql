DELIMITER $$

CREATE FUNCTION Product_Is_Complete(
	in_product_id INT
) 
RETURNS BOOL DETERMINISTIC
BEGIN

    -- This function checks if the given product has values in all the required fields.

    DECLARE is_complete BOOL;
    
    DECLARE product_name VARCHAR(250);
    DECLARE product_category_id INT;
    DECLARE product_location_id INT;
    DECLARE product_dropoff_distance SMALLINT;
    DECLARE product_price_full DECIMAL(10,2);
    
    -- load the product's values into the variables
    SELECT p.name, p.product_categories_sub_id, p.location_id, p.dropoff_distance, p.price_full
    INTO product_name, product_category_id, product_location_id, product_dropoff_distance, product_price_full
    FROM Products p
    WHERE p.id = in_product_id;
    
    -- if any of the required fields are null then the product is NOT complete
    IF ISNULL(product_name) THEN
        SET is_complete = FALSE;
    ELSEIF ISNULL(product_category_id) THEN
        SET is_complete = FALSE;
    ELSEIF ISNULL(product_location_id) THEN
        SET is_complete = FALSE;
    ELSEIF ISNULL(product_dropoff_distance) THEN
        SET is_complete = FALSE;
    ELSEIF ISNULL(product_price_full) THEN
        SET is_complete = FALSE;
    ELSE
        SET is_complete = TRUE;
    END IF;
    
	RETURN (is_complete);
END$$
DELIMITER ;