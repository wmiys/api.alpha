DELIMITER $$
CREATE FUNCTION `Table_To_Text`() RETURNS text CHARSET utf8
    DETERMINISTIC
BEGIN
   DECLARE result TEXT;
   DECLARE name_first CHAR(100);
   DECLARE finished INT DEFAULT 0;
    
    -- create a cursor to loop through all the users rows
    DECLARE cursor_users CURSOR FOR 
    SELECT u.name_first
    FROM Users u
    GROUP BY u.id
    ORDER BY u.id;
    
    -- setup a flag to be set when all the rows have been processed
    DECLARE CONTINUE HANDLER 
    FOR NOT FOUND SET finished = 1;

    OPEN cursor_users;
    SET result = '';
    
    -- for every event id, generate the event's occurrence dates
    LOOP_PROCESS_EVENTS: LOOP
        -- get the next event_id
        FETCH cursor_users INTO name_first;
        
        -- if no more events exit the loop
        IF finished = 1 THEN
            LEAVE LOOP_PROCESS_EVENTS;
        END IF;
        
        IF result = '' THEN
            SET result = name_first;    -- first one
        ELSE
            SET result = CONCAT(result, ';', name_first);   -- prepend a semicolon after the name
        END IF;
    END LOOP LOOP_PROCESS_EVENTS;
    CLOSE cursor_users;
   
    RETURN (result);
    
END$$
DELIMITER ;
