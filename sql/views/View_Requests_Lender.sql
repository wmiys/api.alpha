CREATE VIEW View_Requests_Lender AS 
SELECT 
    r.id AS id,
    r.status AS status,
    r.created_on AS created_on,
    DATE_ADD(r.created_on, INTERVAL 1 DAY) AS expires_on,
    pay.product_id AS product_id,
    p.name AS product_name,
    pay.starts_on AS starts_on,
    pay.ends_on AS ends_on,
    CALCULATE_LENDER_PAYOUT(pay.price_full, pay.fee_lender) AS payout,
    pay.dropoff_location_id AS location_id,
    l.city AS location_city,
    l.state_id AS location_state_id,
    l.state_name AS location_state_name
FROM Product_Requests r
LEFT JOIN Payments pay ON r.payment_id = pay.id
LEFT JOIN Products p ON pay.product_id = p.id
LEFT JOIN Locations l ON pay.dropoff_location_id = l.id
GROUP BY r.id;