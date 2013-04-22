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
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_general_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `site_users`
--

LOCK TABLES `site_users` WRITE;
/*!40000 ALTER TABLE `site_users` DISABLE KEYS */;
INSERT INTO `site_users` VALUES ('admin','c300g','18d119dde31a86ffd3f7f0d2a1314358','ADMIN'),('klient_m1','Клиент мин цена','53be6682d9adfdd8e44427c18afddebe','PRICE_MIN'),('kr_klient','Клиент кр.опт','7c467a3cfcb3a342f6230264c2c0cd53','PRICE_OPT');
/*!40000 ALTER TABLE `site_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-04-22 21:56:04
