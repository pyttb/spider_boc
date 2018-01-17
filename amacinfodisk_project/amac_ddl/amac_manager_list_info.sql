-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: amac
-- ------------------------------------------------------
-- Server version	5.7.20

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
-- Table structure for table `manager_list_info`
--

DROP TABLE IF EXISTS `manager_list_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `manager_list_info` (
  `qry_date` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `id` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `managerName` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `artificialPersonName` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registerNo` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `establishDate` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `managerHasProduct` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registerDate` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registerAddress` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registerProvince` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registerCity` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `regAdrAgg` varchar(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `primaryInvestType` varchar(60) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-15 15:46:11
