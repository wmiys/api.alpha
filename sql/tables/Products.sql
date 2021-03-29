CREATE TABLE `Products` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `name` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `product_categories_sub_id` int(10) unsigned NOT NULL,
  `location_id` int(10) unsigned NOT NULL,
  `price_full` decimal(10,2) unsigned NOT NULL,
  `price_half` decimal(10,2) unsigned NOT NULL,
  `image` char(41) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_categories_sub_id` (`product_categories_sub_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `Products_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `Products_ibfk_2` FOREIGN KEY (`product_categories_sub_id`) REFERENCES `Product_Categories_Sub` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `Products_ibfk_3` FOREIGN KEY (`location_id`) REFERENCES `Locations` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
