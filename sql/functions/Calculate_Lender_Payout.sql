DELIMITER $$
CREATE DEFINER=`rrickgau_main`@`98.223.211.105` FUNCTION `Calculate_Lender_Payout`(
    in_total_price DOUBLE(10,2),
    in_lender_fee DOUBLE (3,2)
) RETURNS double(10,2)
    DETERMINISTIC
BEGIN
	-- This function calculates the total price that the lender would be payed out for
    -- Given the total price and the renter's fee.
    
    DECLARE fee_amount DOUBLE(10,2);
    DECLARE result DOUBLE(10,2);
    
    SET fee_amount = ROUND((in_total_price * (in_lender_fee / 100)), 2);
    SET result = in_total_price - fee_amount;

    RETURN (result);    
END$$
DELIMITER ;
