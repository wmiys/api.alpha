CREATE VIEW View_Product_Requests_Internal AS
SELECT
    -- Product Request
    pr.id AS product_request_id,
    pr.status AS product_request_status,
    pr.responded_on AS product_request_responded_on,
    pr.created_on AS product_request_created_on,
    pr.session_id AS product_request_session_id,
    
    -- Payment
    pay.id AS payment_id,
    pay.dropoff_location_id AS payment_dropoff_location_id,
    pay.starts_on AS payment_starts_on,
    pay.ends_on AS payment_ends_on,
    pay.price_full AS payment_price_full,
    pay.fee_renter AS payment_fee_renter,
    pay.fee_lender AS payment_fee_lender,
    pay.created_on AS payment_created_on,
    
    -- Renter info
    renter.id AS renter_id,
    renter.email AS renter_email,
    renter.name_first AS renter_name_first,
    renter.name_last AS renter_name_last,
    renter.birth_date AS renter_birth_date,
    renter.created_on AS renter_created_on,
    
    -- Product
    p.id AS product_id,
    
    -- Lender info
    lender.id AS lender_id,
    lender.email AS lender_email,
    lender.name_first AS lender_name_first,
    lender.name_last AS lender_name_last,
    lender.birth_date AS lender_birth_date,
    lender.created_on AS lender_created_on
FROM
    Product_Requests pr
    LEFT JOIN Payments pay ON pay.id = pr.payment_id
    LEFT JOIN Users renter ON renter.id = pay.renter_id
    LEFT JOIN Products p ON p.id = pay.product_id
    LEFT JOIN Users lender ON lender.id = p.user_id;