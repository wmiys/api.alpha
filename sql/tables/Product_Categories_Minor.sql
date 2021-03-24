CREATE TABLE `Product_Categories_Minor` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_categories_major_id` INT(10) UNSIGNED NOT NULL,
  `name` CHAR(50) COLLATE UTF8_UNICODE_CI NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `product_categories_major_id` (`product_categories_major_id`),
  CONSTRAINT `Product_Categories_Minor_ibfk_1` FOREIGN KEY (`product_categories_major_id`) REFERENCES `Product_Categories_Major` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE=UTF8_UNICODE_CI;
