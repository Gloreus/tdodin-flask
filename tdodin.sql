CREATE DATABASE  IF NOT EXISTS `odin` /*!40100 DEFAULT CHARACTER SET cp1251 COLLATE cp1251_general_cs */;
USE `odin`;
-- MySQL dump 10.13  Distrib 5.5.16, for Win32 (x86)
--
-- Host: localhost    Database: odin
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Clients`
--

DROP TABLE IF EXISTS `Clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Clients` (
  `ID` int(11) NOT NULL,
  `org_name` varchar(200) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_name` varchar(200) COLLATE cp1251_general_cs NOT NULL,
  `email` varchar(60) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_phone1` varchar(30) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_phone2` varchar(30) COLLATE cp1251_general_cs DEFAULT NULL,
  `address` text COLLATE cp1251_general_cs,
  PRIMARY KEY (`ID`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Orders` (
  `ID` int(11) NOT NULL,
  `org_name` varchar(200) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_name` varchar(200) COLLATE cp1251_general_cs NOT NULL,
  `email` varchar(60) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_phone1` varchar(30) COLLATE cp1251_general_cs DEFAULT NULL,
  `user_phone2` varchar(30) COLLATE cp1251_general_cs DEFAULT NULL,
  `address` text COLLATE cp1251_general_cs,
  `remarks` text COLLATE cp1251_general_cs,
  PRIMARY KEY (`ID`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Photos`
--

DROP TABLE IF EXISTS `Photos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Photos` (
  `id` int(11) NOT NULL,
  `Product_code` varchar(32) COLLATE cp1251_general_cs DEFAULT NULL,
  `size` varchar(10) COLLATE cp1251_general_cs NOT NULL,
  `href` varchar(1000) COLLATE cp1251_general_cs DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_idx` (`Product_code`,`size`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Price`
--

DROP TABLE IF EXISTS `Price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Price` (
  `price_name` varchar(32) COLLATE cp1251_general_cs NOT NULL DEFAULT 'RETAIL' COMMENT 'тип прайса',
  `product_code` varchar(32) COLLATE cp1251_general_cs NOT NULL COMMENT 'ссылка на артикул',
  `value` decimal(15,3) NOT NULL DEFAULT '0.000',
  PRIMARY KEY (`price_name`,`product_code`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TreeItem`
--

DROP TABLE IF EXISTS `TreeItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TreeItem` (
  `code` varchar(32) COLLATE cp1251_general_cs NOT NULL,
  `parent` varchar(32) COLLATE cp1251_general_cs DEFAULT NULL,
  `name` varchar(255) COLLATE cp1251_general_cs NOT NULL DEFAULT '_AUTO_INSERT_',
  `description` text COLLATE cp1251_general_cs NOT NULL,
  `is_node` tinyint(1) NOT NULL DEFAULT '1',
  `countOnStock` int(11) NOT NULL DEFAULT '1' COMMENT 'Остаток на складе',
  PRIMARY KEY (`code`),
  UNIQUE KEY `code_UNIQUE` (`code`),
  KEY `parent_idx` (`parent`,`code`),
  KEY `is_node_idx` (`is_node`,`parent`,`code`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_products`
--

DROP TABLE IF EXISTS `order_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_products` (
  `ID` int(11) NOT NULL,
  `order_ID` int(11) DEFAULT NULL,
  `product_code` varchar(32) COLLATE cp1251_general_cs DEFAULT NULL,
  `product_cnt` int(11) DEFAULT NULL,
  `Ammount` decimal(14,2) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `code_idx` (`product_code`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `site_users`
--

DROP TABLE IF EXISTS `site_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `site_users` (
  `login` varchar(32) COLLATE cp1251_general_cs NOT NULL,
  `user_name` varchar(255) COLLATE cp1251_general_cs DEFAULT NULL,
  `password` char(32) COLLATE cp1251_general_cs NOT NULL,
  `user_group` varchar(32) COLLATE cp1251_general_cs NOT NULL DEFAULT 'RETAIL',
  PRIMARY KEY (`login`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'odin'
--

--
-- Dumping routines for database 'odin'
--
/*!50003 DROP FUNCTION IF EXISTS `add_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `add_order`(
	i_org_name varchar(200),
	i_user_name varchar(200),
	i_email varchar(60),
	i_user_phone1 varchar(30),
	i_user_phone2 varchar(30),
	i_address text,
	i_remarks text
) RETURNS int(11)
BEGIN
	INSERT INTO `odin`.`Orders`
	(
	`org_name`,
	`user_name`,
	`email`,
	`user_phone1`,
	`user_phone2`,
	`address`,
	`remarks`)
	VALUES
	(
	i_org_name,
	i_user_name,
	i_email,
	i_user_phone1,
	i_user_phone2,
	i_address,
	i_remarks);
	

RETURN Last_Insert_ID();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `get_node_by_code` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 FUNCTION `get_node_by_code`(i_code varchar(32), force_add int) RETURNS varchar(32) CHARSET cp1251 COLLATE cp1251_general_cs
BEGIN
  set @res = null;
	if i_code = '' then
		return @res;
	end if;

	select code  into @res from TreeItem t  where  t.code = i_code;
	if @res is not null or force_add < 1 then
		return @res;
	end if;

	set @parent_code = null;
	set @i = locate('.', i_code, 1);
	while  @i > 0 do
		set @s = substring(i_code, 1, @i-1) ;

		set @res = null;
		select code  into @res from TreeItem t  where  t.code = @s;
		if @res is null then
				insert into TreeItem (code, parent,  is_node) 
				values        (@s, @parent_code,  1);
		end if;
		set @parent_code = @s;
		set @i = locate('.', i_code, @i + 1);
	end while;

	insert into TreeItem (code, parent,  is_node) 
		values        (i_code, @parent_code,  1);
	
	RETURN i_code;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `set_node_by_code` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 FUNCTION `set_node_by_code`(i_code varchar(32), i_name varchar(255), i_desc text, force_add int) RETURNS varchar(32) CHARSET cp1251 COLLATE cp1251_general_cs
BEGIN
	set @node = NULL;
	if force_add > 0 then	
		set @node  = get_node_by_code(i_code, 1);
		update TreeItem t set
			t.name = i_name,
			t.description = i_desc
		where code = @node;
	else
		update TreeItem t set
			t.name = i_name,
			t.description = i_desc
		where t.code = i_code;
		if Row_count() > 0 then
			set @node = i_code;
		end if;
	end if;		
RETURN @node;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `set_product` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 FUNCTION `set_product`(i_code varchar(32), i_parent varchar(32), i_name varchar(255), i_desc text, force_add int) RETURNS varchar(32) CHARSET cp1251 COLLATE cp1251_general_cs
BEGIN
	set @res = null;
	select code into @res from TreeItem t
	where t.code = i_code and t.parent = i_parent;

	if @res is null and force_add > 0 then
		insert into TreeItem (code, parent, name, description, is_node) 
		values (i_code, i_parent, i_name, i_desc, 0);
		set @res = i_code;
	else
		update TreeItem t set
			t.name = i_name,
			t.description = i_desc
		where t.code = @res;
	end if;
RETURN @res;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_basket_by_codes` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `get_basket_by_codes`(
	in i_codes varchar(4096),
	in i_price_name varchar(32))
BEGIN
	-- i_codes строка вида "(cod1,cod2,cod3) " co скобками
	-- Без цены товар не продаём!
	set @q = CONCAT("
		select t.code, hex(t.code) as hcode, t.name, p.value as price from
		TreeItem t
			join Price p on p.price_name = '", i_price_name,  "'
		    and p.product_code = t.code
		where
			t.is_node = 0
			and t.code in ",  i_codes);
	prepare q_sql from @q;
	execute q_sql;
	deallocate prepare q_sql; 
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_path_by_code` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `get_path_by_code`(in i_code varchar(32))
BEGIN
	set @node = NULL;
	select t.parent into @node from TreeItem t where t.code = i_code;
	if @node > '' then 
		select t.code, t.name  from TreeItem t
		where position(t.code in @node) =  1;
	end if;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_product` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 PROCEDURE `get_product`(in i_code varchar(32), in i_price_name varchar(32))
BEGIN
	select
		  t.code
		, t.name
		, t.description
		, p.value as price
		, ph1.href as large_image_url
		, ph2.href as full_image_url
    from
		TreeItem t
		left join Price p on p.price_name = i_price_name and p.product_code = t.code
		left join Photos ph1 on t.code = ph1.product_code and ph1.size = 'L'
		left join Photos ph2 on t.code = ph2.product_code and ph2.size = 'orig'
	
	where
		t.is_node = 0
		and t.code = i_code
	order by t.code;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_products` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 PROCEDURE `get_products`(in i_code varchar(32), in i_price_name varchar(32))
BEGIN
	select t.code, hex(t.code) as hcode, t.name, t.description, ph.href as small_image_url, p.value as price from
	TreeItem t
		left join Price p on p.price_name = i_price_name and p.product_code = t.code
		left join Photos ph on t.code = ph.product_code and ph.size = 'XS'
	where
		t.is_node = 0
		and t.parent = i_code
	order by t.code;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `set_photo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `set_photo`(in i_code varchar(32), in i_size varchar(10), in i_href varchar(1000), in i_width int, in i_height int)
BEGIN
	insert into Photos (product_code, size, href, width, height)
	values(i_code, i_size, i_href, i_width, i_height)
	ON DUPLICATE KEY UPDATE
		href = i_href,
		width = i_width,
		height = i_height;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `set_price` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`odin`@`192.168.0.10`*/ /*!50003 PROCEDURE `set_price`(in i_code varchar(32), in i_price_name varchar(32), in i_price decimal(15, 3))
BEGIN
	insert into Price (price_name, product_code, `value`) 
		values(i_price_name, i_code, i_price)	
	ON DUPLICATE KEY UPDATE
		`value` = i_price;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-04-25 23:20:16
