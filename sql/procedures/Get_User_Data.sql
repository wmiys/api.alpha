DELIMITER $$
CREATE DEFINER=`main`@`%` PROCEDURE `Get_User_Data`(
    IN in_user_id INT UNSIGNED
)
BEGIN

    /************************************************************************
    Create some temporary tables to hold all the data we're going to return
    *************************************************************************/
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Products LIKE Products;
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Product_Availabilities LIKE Product_Availability;
	CREATE TEMPORARY TABLE IF NOT EXISTS User_Product_Images LIKE Product_Images;
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Product_Request_Received SELECT * FROM View_Product_Requests_Internal v WHERE v.product_request_id IS NULL;
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Product_Request_Submitted SELECT * FROM View_Product_Requests_Internal v WHERE v.product_request_id IS NULL;
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Balance_Transfers LIKE Balance_Transfers;
    CREATE TEMPORARY TABLE IF NOT EXISTS User_Payout_Accounts LIKE Payout_Accounts;
    
    /************************************************************************
    Fill all the temporary data with the user's data
    *************************************************************************/
    -- Products
    INSERT INTO User_Products
    SELECT * FROM Products p
    WHERE p.user_id = in_user_id;

    -- Product Availability
    INSERT INTO User_Product_Availabilities
    SELECT * FROM Product_Availability pa
    WHERE EXISTS (
		SELECT 1 FROM User_Products p
        WHERE p.id = pa.product_id
	);
    
    -- Product Images
    INSERT INTO User_Product_Images
    SELECT * FROM Product_Images pi
    WHERE EXISTS (
		SELECT 1 FROM User_Products p
        WHERE p.id = pi.product_id
	);
    
    -- Received product requests
    INSERT INTO User_Product_Request_Received
    SELECT * FROM View_Product_Requests_Internal v
    WHERE EXISTS (
		SELECT 1 FROM User_Products p
        WHERE p.id = v.payment_product_id
    );
    
    -- Submitted product requests
    INSERT INTO User_Product_Request_Submitted
    SELECT * FROM View_Product_Requests_Internal v
    WHERE v.renter_id = in_user_id;
    
    -- Balance Transfers
	INSERT INTO User_Balance_Transfers
    SELECT * FROM Balance_Transfers b
    WHERE b.user_id = in_user_id;
    
    -- Payout accounts
	INSERT INTO User_Payout_Accounts
    SELECT * FROM Payout_Accounts pa
    WHERE pa.user_id = in_user_id;
    
    /************************************************************************
    Return all the record sets to the caller
    *************************************************************************/
	SELECT * FROM User_Products;
    SELECT * FROM User_Product_Availabilities;
	SELECT * FROM User_Product_Images;
    SELECT * FROM User_Product_Request_Received;
    SELECT * FROM User_Product_Request_Submitted;
    SELECT * FROM User_Balance_Transfers;
    SELECT * FROM User_Payout_Accounts;
    
    /************************************************************************
    Drop the temporary tables
    *************************************************************************/
	DROP TABLE User_Products;
	DROP TABLE User_Product_Availabilities;
	DROP TABLE User_Product_Images;
    DROP TABLE User_Product_Request_Received;
    DROP TABLE User_Product_Request_Submitted;
    DROP TABLE User_Balance_Transfers;
    DROP TABLE User_Payout_Accounts;

END$$
DELIMITER ;
