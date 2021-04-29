DELIMITER $$
CREATE PROCEDURE `Get_Locations_In_Range`(
    IN location_id INT UNSIGNED,
    IN num_miles INT UNSIGNED
)
BEGIN    
    -- select only locations that fall within the given mile range
	SELECT 
		loc.id                                  AS id,
		loc.city                                AS city,
		loc.state_id                            AS state_id,
		loc.state_name                          AS state_name,
		loc.lat                                 AS lat,
		loc.lng                                 AS lng,
		loc.population                          AS population,
		loc.ranking                             AS ranking,
		loc.county_name                         AS county_name,
		ROUND(MILES_BETWEEN(location_id, id))   AS distance
	FROM Locations loc
	WHERE loc.id != location_id
	GROUP BY loc.id
	HAVING distance <= num_miles
	ORDER BY distance ASC; 
END$$
DELIMITER ;
