DELIMITER $$
CREATE PROCEDURE `Search_Locations`(
    IN keyword_query TEXT,
    IN num_results TINYINT UNSIGNED
)
BEGIN
    -- create the temp table to hold the location ids and FTS match scores
    CREATE TEMPORARY TABLE IF NOT EXISTS Temp_Locations_Search (
        id INT UNSIGNED NOT NULL UNIQUE,
        fts_score DECIMAL (10, 6) NOT NULL
    );
    
    -- add all the locations and their FTS match scores to the temp table
    INSERT INTO Temp_Locations_Search (id, fts_score) 
    (
        SELECT 
            loc.id, 
            MATCH (city) AGAINST (keyword_query) AS fts_score
        FROM Locations loc 
    );
    
    -- return the locations ordered by fts score, ranking, then population
    SELECT 
        t.id AS             id, 
        l.city AS             city, 
        l.state_id AS         state_id, 
        l.state_name AS     state_name,
        l.lat AS             lat,
        l.lng AS             lng,
        l.ranking AS         ranking,
        l.population AS     population,
        l.county_name AS     county_name
    FROM Temp_Locations_Search t
    LEFT JOIN Locations l ON l.id = t.id
    ORDER BY t.fts_score DESC, l.ranking ASC, l.population DESC
    LIMIT NUM_RESULTS;
    
    DROP TEMPORARY TABLE Temp_Locations_Search;
END$$
DELIMITER ;
