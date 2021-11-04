DELIMITER $$
CREATE DEFINER=`main`@`%` FUNCTION `Calculate_Lender_Balance`(
	in_user_id INT
) RETURNS double
    DETERMINISTIC
BEGIN
    DECLARE balance DOUBLE;
    DECLARE sum_earnings DOUBLE;
    
    -- calculate the lenders earnings
    SELECT SUM(CALCULATE_LENDER_PAYOUT(pay.price_full, pay.fee_lender, pay.starts_on, pay.ends_on))
    INTO sum_earnings
    FROM Payments pay 
        INNER JOIN Product_Requests pr 
            ON pr.payment_id = pay.id 
            AND pr.status = 'accepted'
    WHERE pay.product_id IN 
        (SELECT p.id FROM Products p WHERE p.user_id = in_user_id);    
    
    
    -- Don't want to return a null
    IF ISNULL(sum_earnings) THEN
        SET balance = 0;
    ELSE
        SET balance = sum_earnings;
    END IF;
    
    RETURN (balance);
END$$
DELIMITER ;
