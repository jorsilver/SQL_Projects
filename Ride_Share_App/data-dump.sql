-- MySQL dump 10.13  Distrib 8.0.36, for macos14 (arm64)
--
-- Host: localhost    Database: RideShare2
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `VIN` varchar(17) NOT NULL,
  `OwnerID` int NOT NULL,
  `PlateNum` varchar(10) NOT NULL,
  `Make` varchar(50) NOT NULL,
  `Model` varchar(50) NOT NULL,
  `Available` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`VIN`),
  KEY `OwnerID` (`OwnerID`),
  CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`OwnerID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES ('1GYS4KKJ4GR100001',2,'QHW6485','Cadillac','Escalade',0),('3VWCK21C71M400001',1,'J25HF39','Audi','Q3',0),('4T1BF1FK0GU000001',2,'RJL7142','Toyota','Camry',0),('JH2PC4006FK200001',1,'4XPT894','Honda','Acord',0);
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`newuser`@`%`*/ /*!50003 TRIGGER `update_arrival_Time` AFTER UPDATE ON `cars` FOR EACH ROW BEGIN
    IF NEW.Available = 1 THEN
        UPDATE rides
        SET arvlTime = NOW()
        WHERE Vin = NEW.VIN AND arvlTime IS NULL;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rides`
--

DROP TABLE IF EXISTS `rides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rides` (
  `RideID` int NOT NULL AUTO_INCREMENT,
  `RiderID` int NOT NULL,
  `DriverID` int DEFAULT NULL,
  `VIN` varchar(17) DEFAULT NULL,
  `ReqTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `arvlTime` timestamp NULL DEFAULT NULL,
  `DriverRtg` decimal(3,2) DEFAULT NULL,
  `RiderRtg` decimal(3,2) DEFAULT NULL,
  `PickUpAdr` varchar(255) DEFAULT NULL,
  `DropOffAdr` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`RideID`),
  KEY `RiderID` (`RiderID`),
  KEY `DriverID` (`DriverID`),
  KEY `VIN` (`VIN`),
  CONSTRAINT `rides_ibfk_1` FOREIGN KEY (`RiderID`) REFERENCES `users` (`userID`),
  CONSTRAINT `rides_ibfk_2` FOREIGN KEY (`DriverID`) REFERENCES `users` (`userID`),
  CONSTRAINT `rides_ibfk_3` FOREIGN KEY (`VIN`) REFERENCES `cars` (`VIN`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rides`
--

LOCK TABLES `rides` WRITE;
/*!40000 ALTER TABLE `rides` DISABLE KEYS */;
INSERT INTO `rides` VALUES (1,3,1,'JH2PC4006FK200001','2024-04-12 17:08:21','2024-04-12 17:09:41',4.60,4.60,'123 Main Street','456 Elm Avenue'),(2,4,2,'4T1BF1FK0GU000001','2024-04-12 17:12:26','2024-04-12 17:13:46',4.50,4.50,'369 Cedar Avenue','579 Willow Road'),(3,3,2,'1GYS4KKJ4GR100001','2024-04-20 04:35:28','2024-04-20 04:37:54',4.70,4.70,'246 Oak Lane','135 Birch Street'),(4,4,1,'3VWCK21C71M400001','2024-04-20 04:35:29','2024-04-20 04:38:17',4.80,4.80,'789 Maple Drive','987 Pine Street');
/*!40000 ALTER TABLE `rides` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `ActType` enum('Rider','Driver') NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Jordan','p','Driver'),(2,'Thomas','p','Driver'),(3,'Bob','p','Rider'),(4,'Lisa','p','Rider');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-19 22:43:32
