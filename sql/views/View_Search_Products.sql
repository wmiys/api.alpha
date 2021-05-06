CREATE VIEW `View_Search_Products` AS
    SELECT 
        `p`.`id` AS `id`,
        `p`.`name` AS `name`,
        `p`.`description` AS `description`,
        `p`.`product_categories_sub_id` AS `product_categories_sub_id`,
        `sub`.`name` AS `product_categories_sub_name`,
        `sub`.`product_categories_minor_id` AS `product_categories_minor_id`,
        `minor`.`name` AS `product_categories_minor_name`,
        `minor`.`product_categories_major_id` AS `product_categories_major_id`,
        `major`.`name` AS `product_categories_major_name`,
        `p`.`dropoff_distance` AS `dropoff_distance`,
        `p`.`price_full` AS `price_full`,
        `p`.`price_half` AS `price_half`,
        `p`.`image` AS `image`,
        `p`.`minimum_age` AS `minimum_age`,
        `p`.`user_id` AS `user_id`,
        `u`.`name_first` AS `user_name_first`,
        `u`.`name_last` AS `user_name_last`
    FROM
        ((((`Products` `p`
        LEFT JOIN `Product_Categories_Sub` `sub` ON ((`p`.`product_categories_sub_id` = `sub`.`id`)))
        LEFT JOIN `Product_Categories_Minor` `minor` ON ((`sub`.`product_categories_minor_id` = `minor`.`id`)))
        LEFT JOIN `Product_Categories_Major` `major` ON ((`minor`.`product_categories_major_id` = `major`.`id`)))
        LEFT JOIN `Users` `u` ON ((`p`.`user_id` = `u`.`id`)));
