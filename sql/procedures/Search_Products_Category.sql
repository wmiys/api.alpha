DELIMITER $$
CREATE PROCEDURE `Search_Products_Category`(
    IN in_dropoff_location_id INT UNSIGNED,
    IN in_starts_on DATE,
    IN in_ends_on DATE,
    IN in_product_categories_type TINYINT UNSIGNED,
    IN in_product_categories_id INT UNSIGNED
)
BEGIN

    DECLARE product_category_type_major TINYINT DEFAULT 1;
    DECLARE product_category_type_minor TINYINT DEFAULT 2;
    DECLARE product_category_type_sub TINYINT DEFAULT 3;

    CREATE TEMPORARY TABLE IF NOT EXISTS tmp_products_available (
		product_id INT UNSIGNED
	);
    
    Call Search_Products_Setup(in_dropoff_location_id, in_starts_on, in_ends_on);
    
    IF in_product_categories_type = product_category_type_major THEN                -- major categories
        SELECT * FROM View_Search_Products vp
        WHERE 
            vp.id IN (SELECT * FROM tmp_products_available)
            AND vp.product_categories_major_id = in_product_categories_id;
    ELSEIF in_product_categories_type = product_category_type_minor THEN            -- minor categories
        SELECT * FROM View_Search_Products vp
        WHERE 
            vp.id IN (SELECT * FROM tmp_products_available)
            AND vp.product_categories_minor_id = in_product_categories_id;
    ELSEIF in_product_categories_type = product_category_type_sub THEN              -- sub categories
        SELECT * FROM View_Search_Products vp
        WHERE 
            vp.id IN (SELECT * FROM tmp_products_available)
            AND vp.product_categories_sub_id = in_product_categories_id;
    END IF;
	
    DROP TEMPORARY TABLE tmp_products_available;

END$$
DELIMITER ;
