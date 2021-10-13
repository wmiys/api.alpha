DELIMITER $$
CREATE FUNCTION `Calculate_Lender_Payout`(
    in_daily_price DOUBLE(10,2),
    in_lender_fee DOUBLE (3,2),
    in_starts_on DATE,
    in_ends_on DATE
) RETURNS DOUBLE(10,2)
    DETERMINISTIC
BEGIN
	-- This function calculates the total price that the lender would be payed out for
    -- Given the total price and the renter's fee.
    
    DECLARE fee_amount DOUBLE(10,2);
    DECLARE result DOUBLE(10,2);
    DECLARE num_days INT;
    DECLARE sub_total DOUBLE(10,2);
    
    SET num_days = DATEDIFF(in_ends_on, in_starts_on);
    
    SET sub_total = num_days * in_daily_price;
    
    SET fee_amount = ROUND((sub_total * (in_lender_fee / 100)), 2);
    
    SET result = sub_total - fee_amount;

    RETURN (result);    
END$$
DELIMITER ;
