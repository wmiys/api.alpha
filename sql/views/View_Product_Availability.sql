CREATE VIEW `View_Product_Availability`
AS
  SELECT `a`.`id`         AS `id`,
         `a`.`product_id`  AS `product_id`,
         `a`.`starts_on`  AS `starts_on`,
         `a`.`ends_on`    AS `ends_on`,
         `a`.`note`       AS `note`,
         `a`.`created_on` AS `created_on`
  FROM   `Product_Availability` `a`; 