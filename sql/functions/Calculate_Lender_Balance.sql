CREATE DEFINER=`main`@`%` FUNCTION `Calculate_Lender_Balance`(
	in_user_id INT UNSIGNED
) RETURNS double
    DETERMINISTIC
BEGIN

 	DECLARE range_start TIMESTAMP;
    DECLARE balance DOUBLE;
    
    -- retrieve the most recent balance transfer date
    SELECT bt.created_on
    INTO range_start
    FROM Balance_Transfers bt
    WHERE bt.user_id = in_user_id 
    ORDER BY bt.created_on DESC
    LIMIT 1;
    
    -- if this is the first one, set the range start to 2020
    IF ISNULL(range_start) THEN
		SET range_start = '2020-01-01';
	END IF;
    
	-- calculate the lenders earnings
    SELECT SUM(CALCULATE_LENDER_PAYOUT(pay.price_full, pay.fee_lender, pay.starts_on, pay.ends_on))
    INTO balance
    FROM Payments pay 
        INNER JOIN Product_Requests pr 
            ON pr.payment_id = pay.id 
            AND pr.status = 'accepted'
    WHERE EXISTS (
		SELECT 1 FROM Products p 
        WHERE p.user_id = in_user_id 
        AND p.id = pay.product_id 
        AND (
			pay.ends_on >= range_start 
            AND pay.ends_on < CURRENT_TIMESTAMP()
		)
	);
    
    -- make if the lender has no records, return 0
    IF ISNULL(balance) THEN
		SET balance = 0;
	END IF;
        
        
    RETURN (balance);

END