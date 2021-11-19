CREATE VIEW `View_Payments_Internal` AS
    SELECT 
        `pay`.`id` AS `id`,
        `pay`.`product_id` AS `product_id`,
        `prod`.`name` AS `product_name`,
        `prod`.`user_id` AS `lender_id`,
        `pay`.`renter_id` AS `renter_id`,
        `u`.`name_first` AS `renter_name_first`,
        `u`.`name_last` AS `renter_name_last`,
        `pay`.`dropoff_location_id` AS `dropoff_location_id`,
        `pay`.`starts_on` AS `starts_on`,
        `pay`.`ends_on` AS `ends_on`,
        ((TO_DAYS(`pay`.`ends_on`) - TO_DAYS(`pay`.`starts_on`)) + 1) AS `num_days`,
        `pay`.`price_full` AS `price_full`,
        `pay`.`fee_renter` AS `fee_renter`,
        `pay`.`fee_lender` AS `fee_lender`,
        (SELECT (`num_days` * `prod`.`price_full`)) AS `total_price`,
        (SELECT CALCULATE_RENTER_PRICE(`total_price`, `pay`.`fee_renter`)) AS `total_renter_fee`,
        CALCULATE_LENDER_PAYOUT(`pay`.`price_full`,
                `pay`.`fee_lender`,
                `pay`.`starts_on`,
                `pay`.`ends_on`) AS `total_payout_lender`
    FROM
        ((`Payments` `pay`
        LEFT JOIN `Products` `prod` ON ((`pay`.`product_id` = `prod`.`id`)))
        LEFT JOIN `Users` `u` ON ((`pay`.`renter_id` = `u`.`id`)))
    GROUP BY `pay`.`id`;
