DELIMITER $$
CREATE PROCEDURE `Search_Locations`(
    IN keyword_query TEXT,
    IN num_results TINYINT UNSIGNED
)
BEGIN    
    -- return the locations that are like the query passed in
    SELECT 
        l.id AS             id, 
        l.city AS           city, 
        l.state_id AS       state_id, 
        l.state_name AS     state_name,
        l.lat AS            lat,
        l.lng AS            lng,
        l.ranking AS        ranking,
        l.population AS     population,
        l.county_name AS    county_name
    FROM Locations l
    WHERE CONCAT(l.city, ' ', l.state_id, ' ', l.state_name) LIKE CONCAT('%', keyword_query, '%')
    ORDER BY l.ranking ASC, l.population DESC
    LIMIT NUM_RESULTS;
END$$
DELIMITER ;
