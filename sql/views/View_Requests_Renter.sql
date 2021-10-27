CREATE VIEW View_Requests_Renter AS
SELECT 
    pr.id AS id,
    pr.status AS status,
    pr.created_on AS created_on,
    pay.renter_id AS renter_id,
    pay.product_id AS product_id,
    p.name AS product_name,
    p.image AS product_image,
    pay.starts_on AS starts_on,
    pay.ends_on AS ends_on,
    ((TO_DAYS(pay.ends_on) - TO_DAYS(pay.starts_on)) + 1) AS `num_days`,
    pay.price_full AS price_full,
    (SELECT (num_days * pay.price_full)) AS `price_total`,
    (SELECT CALCULATE_RENTER_PRICE(`price_total`, `pay`.`fee_renter`)) AS `fee_renter`,
    pay.dropoff_location_id AS location_id,
    l.city AS location_city,
    l.state_id AS location_state_id,
    l.state_name AS location_state_name
FROM
    Product_Requests pr
        LEFT JOIN Payments pay ON pay.id = pr.payment_id
        LEFT JOIN Products p ON p.id = pay.product_id
        LEFT JOIN Locations l ON l.id = pay.dropoff_location_id;
