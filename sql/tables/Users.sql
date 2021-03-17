CREATE TABLE `Users` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` CHAR(254) COLLATE UTF8_UNICODE_CI NOT NULL,
  `password` CHAR(255) COLLATE UTF8_UNICODE_CI NOT NULL,
  `name_first` CHAR(100) COLLATE UTF8_UNICODE_CI NOT NULL,
  `name_last` CHAR(150) COLLATE UTF8_UNICODE_CI NOT NULL,
  `birth_date` DATE NOT NULL,
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE=UTF8_UNICODE_CI;
