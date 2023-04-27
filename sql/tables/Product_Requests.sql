CREATE TABLE `Product_Requests` (
  `id` CHAR(36) NOT NULL,
  `payment_id` CHAR(36) NOT NULL,
  `session_id` CHAR(255) NOT NULL,
  `status` ENUM('pending','accepted','denied','expired') NOT NULL DEFAULT 'pending',
  `responded_on` DATETIME DEFAULT NULL,
  `review_score` TINYINT UNSIGNED DEFAULT NULL,
  `review_comment` VARCHAR(500) DEFAULT NULL,
  `created_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `payment_id` (`payment_id`),
  CONSTRAINT `Product_Requests_ibfk_1` FOREIGN KEY (`payment_id`) REFERENCES `Payments` (`id`) ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_0900_AI_CI;
