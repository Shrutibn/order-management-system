CREATE TABLE `order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` varchar(40) DEFAULT NULL,
  `user_id` varchar(40) NOT NULL,
  `item_ids` varchar(100) NOT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `order_status` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`)
);