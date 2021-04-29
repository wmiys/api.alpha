DELIMITER $$
CREATE DEFINER=`rrickgau_main`@`24.13.68.79` FUNCTION `Miles_Between`(
	location_id_1 INT UNSIGNED,
    location_id_2 INT UNSIGNED
) RETURNS double
    DETERMINISTIC
BEGIN
	DECLARE lat1 DECIMAL(11,7);
	DECLARE lng1 DECIMAL(11,7);
	DECLARE lat2 DECIMAL(11,7);
	DECLARE lng2 DECIMAL(11,7);
    
    SELECT l.lat, l.lng INTO lat1, lng1 FROM Locations l WHERE l.id = location_id_1;	-- get the first location lat/lng points
    SELECT l.lat, l.lng INTO lat2, lng2 FROM Locations l WHERE l.id = location_id_2;	-- get the second location lat/lng points
    
RETURN ACOS( SIN(lat1*PI()/180)*SIN(lat2*PI()/180) + COS(lat1*PI()/180)*COS(lat2*PI()/180)*COS(lng2*PI()/180-lng1*PI()/180) ) * 3959;
END$$
DELIMITER ;
