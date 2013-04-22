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
-- Dumping events for database 'odin'
--

--
-- Dumping routines for database 'odin'
--
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
	select t.code, t.name, t.description, ph.href as small_image_url, p.value as price from
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

-- Dump completed on 2013-04-22 21:56:06
