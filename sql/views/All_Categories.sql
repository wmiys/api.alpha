CREATE 
    ALGORITHM = UNDEFINED 
    SQL SECURITY DEFINER
VIEW `All_Categories` AS
    SELECT 
        `major`.`id` AS `major_id`,
        `major`.`name` AS `major_name`,
        `minor`.`id` AS `minor_id`,
        `minor`.`name` AS `minor_name`,
        `sub`.`id` AS `sub_id`,
        `sub`.`name` AS `sub_name`
    FROM
        ((`Product_Categories_Sub` `sub`
        LEFT JOIN `Product_Categories_Minor` `minor` ON ((`sub`.`product_categories_minor_id` = `minor`.`id`)))
        LEFT JOIN `Product_Categories_Major` `major` ON ((`minor`.`product_categories_major_id` = `major`.`id`)))
    GROUP BY `sub`.`id`;
