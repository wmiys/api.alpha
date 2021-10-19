DELIMITER $$
CREATE FUNCTION Ranges_Conflict (
	in_range1_starts_on DATE,
    in_range1_ends_on DATE,
    in_range2_starts_on DATE,
    in_range2_ends_on DATE
) 
RETURNS BOOL DETERMINISTIC
BEGIN
    -- This function checks if a given range falls within another range.
    DECLARE result BOOL DEFAULT FALSE;
    DECLARE next_date DATE DEFAULT in_range1_starts_on;
    
    LOOP_LABEL: LOOP
        -- verify that the current date is still within the range
        IF  next_date > in_range1_ends_on THEN 
            LEAVE LOOP_LABEL;
        END  IF;
        
        -- if the current date falls within the range, return true
        IF DATE_IN_RANGE(next_date, in_range2_starts_on, in_range2_ends_on) = TRUE THEN
            SET result = TRUE;
            LEAVE LOOP_LABEL;
        END IF;
        
        -- go to the next date
        SET next_date = DATE_ADD(next_date, INTERVAL 1 DAY);
    END LOOP;
    
	RETURN (result);
END$$
DELIMITER ;