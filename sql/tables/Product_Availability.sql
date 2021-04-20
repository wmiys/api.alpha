CREATE TABLE `Product_Availability` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `product_id` INT(10) UNSIGNED NOT NULL,
    `starts_on` DATE NOT NULL,
    `ends_on` DATE NOT NULL,
    `note` TEXT COLLATE UTF8_UNICODE_CI,
    `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `Product_Availability_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8 COLLATE=UTF8_UNICODE_CI;
