CREATE DEFINER=`rrickgau_main`@`98.223.211.105` FUNCTION `Calculate_Renter_Price`(
    in_total_price DOUBLE(10,2),
    in_renter_fee DOUBLE (3,2)
) RETURNS double(10,2)
    DETERMINISTIC
BEGIN
	-- This function calculates the total price that the renter will have to pay
    -- Given the total price and the renter's fee.
    
    DECLARE fee_amount DOUBLE(10,2);
    DECLARE result DOUBLE(10,2);
    
    SET fee_amount = ROUND((in_total_price * (in_renter_fee / 100)), 2);
    SET result = fee_amount + in_total_price;
    
    RETURN (result);    
END