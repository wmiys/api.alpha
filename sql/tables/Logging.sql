
-- This is used for logging purposes.

CREATE TABLE `Logging` (
    `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `message1` TEXT,
    `message2` TEXT,
    `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;
