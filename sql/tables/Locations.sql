CREATE TABLE `Locations` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(100) COLLATE UTF8_UNICODE_CI NOT NULL,
  `locations_states_id` INT(10) UNSIGNED NOT NULL,
  `lat` DECIMAL(4,4) NOT NULL,
  `lng` DECIMAL(4,4) NOT NULL,
  `population` BIGINT(20) DEFAULT NULL,
  `ranking` INT(11) DEFAULT NULL,
  `county_name` VARCHAR(150) COLLATE UTF8_UNICODE_CI DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `locations_states_id` (`locations_states_id`),
  CONSTRAINT `Locations_ibfk_1` FOREIGN KEY (`locations_states_id`) REFERENCES `Locations_States` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE=UTF8_UNICODE_CI;
