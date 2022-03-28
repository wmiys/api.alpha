CREATE TABLE `Product_Images` (
    `id` CHAR(36) NOT NULL,
    `product_id` INT UNSIGNED NOT NULL,
    `file_name` CHAR(50) NOT NULL,
    `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`),
    UNIQUE KEY `file_name_UNIQUE` (`file_name`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `Product_Images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products` (`id`) ON
    UPDATE
        CASCADE
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB3;