DELIMITER $$
CREATE FUNCTION Date_In_Range (
    in_date DATE,
    in_range_start DATE,
    in_range_end DATE
)
RETURNS BOOL
DETERMINISTIC
BEGIN
    -- Checks to see if the given date falls within the given start and end date
    -- Assumes that in_range_start < in_range_end
    DECLARE result BOOL;

    IF in_date < in_range_start THEN
        SET result = FALSE;
    ELSEIF in_date > in_range_end THEN
        SET result = FALSE;
    ELSE
        SET result = TRUE;
    END IF;
    
	-- return the result
	RETURN (result);

END$$
DELIMITER ;