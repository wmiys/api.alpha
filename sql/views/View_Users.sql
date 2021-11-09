CREATE VIEW `View_Users` AS
SELECT 
    `u`.`id` AS `id`,
    `u`.`email` AS `email`,
    `u`.`name_first` AS `name_first`,
    `u`.`name_last` AS `name_last`,
    `u`.`birth_date` AS `birth_date`,
    `u`.`created_on` AS `created_on`,
    (SELECT 
            COUNT(0)
        FROM
            `Products` `p2`
        WHERE
            (`p2`.`user_id` = `u`.`id`)) AS `count_products`,
    COUNT(`pr`.`id`) AS `count_agreements`,
    CALCULATE_LENDER_EARNINGS(`u`.`id`) AS `lender_balance`,
    `pa`.`account_id` AS `payout_account_id`
FROM
    ((((`Users` `u`
    LEFT JOIN `Products` `p` ON ((`p`.`user_id` = `u`.`id`)))
    LEFT JOIN `Payments` `pay` ON ((`pay`.`product_id` = `p`.`id`)))
    LEFT JOIN `Product_Requests` `pr` ON (((`pr`.`payment_id` = `pay`.`id`)
        AND (`pr`.`status` = 'accepted'))))
    LEFT JOIN `Payout_Accounts` `pa` ON (((`pa`.`user_id` = `u`.`id`)
        AND (`pa`.`confirmed` = TRUE))))
GROUP BY `u`.`id`