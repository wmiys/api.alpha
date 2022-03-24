DELIMITER $$
CREATE PROCEDURE `Finalize_Password_Reset`(
    IN in_password_reset_id CHAR(36),
    IN in_updated_on TIMESTAMP,
    IN in_new_password CHAR(255),
    IN in_num_minutes_expires INT
)
BEGIN

	DECLARE user_email CHAR(254);
	DECLARE user_id INT;
	DECLARE minutes_since_created_on INT;
	DECLARE num_records INT DEFAULT -1;
	DECLARE existing_updated_on_value TIMESTAMP;
	
    -- Fetch all the data we need to verify that the password reset record is valid
	SELECT
		pr.email AS pr_email,
		u.id AS user_id,
		pr.updated_on,
		ABS(TIMESTAMPDIFF(MINUTE, pr.created_on, in_updated_on)) AS created_on_diff 
	INTO 
		user_email,
		user_id,
		existing_updated_on_value,
		minutes_since_created_on
	FROM
		Password_Resets pr
		LEFT JOIN Users u ON u.email = pr.email
	WHERE
		pr.id = in_password_reset_id
	LIMIT
		1;

SP_BLOCK: BEGIN 
	
    SET num_records = -1;
    
    -- valid password_reset_id and email belongs to a User's account
	IF COALESCE(user_email, user_id, minutes_since_created_on) IS NULL THEN 
		LEAVE SP_BLOCK;	
	
    -- reset record does not already have an updated_on value
    ELSEIF existing_updated_on_value IS NOT NULL THEN 
		LEAVE SP_BLOCK;
	
    -- password reset record is not expired
	ELSEIF minutes_since_created_on > in_num_minutes_expires THEN 
		LEAVE SP_BLOCK;		
    END IF;

	-- update the password reset table
	UPDATE Password_Resets 
	SET updated_on = in_updated_on
	WHERE id = in_password_reset_id;

	-- update the user's password in the Users table
	UPDATE Users
	SET password = in_new_password
	WHERE id = user_id;

	SET num_records = 1;

END SP_BLOCK;

-- returns 1 if successful, otherwise it returns -1
SELECT num_records AS rowcount;
    
END$$
DELIMITER ;
