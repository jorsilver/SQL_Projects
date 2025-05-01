-- MySQL dump 10.13  Distrib 8.0.36, for macos14 (arm64)
--
-- Host: localhost    Database: Fitness
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
-- Table structure for table `daily_log`
--

DROP TABLE IF EXISTS `daily_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `total_caloric_burn` int DEFAULT NULL,
  `total_caloric_intake` int DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `daily_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_log`
--

LOCK TABLES `daily_log` WRITE;
/*!40000 ALTER TABLE `daily_log` DISABLE KEYS */;
INSERT INTO `daily_log` VALUES (1,1,'2024-04-29',784,2154,'Leg day, '),(2,1,'2024-05-01',702,2026,'Chest day'),(3,1,'2024-05-02',700,2000,'test');
/*!40000 ALTER TABLE `daily_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily_log_meal`
--

DROP TABLE IF EXISTS `daily_log_meal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily_log_meal` (
  `log_id` int NOT NULL,
  `meal_id` int NOT NULL,
  `time` time NOT NULL,
  `servings` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`log_id`,`meal_id`),
  KEY `meal_id` (`meal_id`),
  CONSTRAINT `daily_log_meal_ibfk_1` FOREIGN KEY (`log_id`) REFERENCES `daily_log` (`log_id`),
  CONSTRAINT `daily_log_meal_ibfk_2` FOREIGN KEY (`meal_id`) REFERENCES `meal` (`meal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_log_meal`
--

LOCK TABLES `daily_log_meal` WRITE;
/*!40000 ALTER TABLE `daily_log_meal` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_log_meal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise`
--

DROP TABLE IF EXISTS `exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exercise` (
  `exercise_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(35) NOT NULL,
  `muscle_group` varchar(35) NOT NULL,
  `description` text,
  `MET_value` decimal(5,2) DEFAULT NULL,
  `10_reps_time_secs` int DEFAULT NULL,
  PRIMARY KEY (`exercise_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise`
--

LOCK TABLES `exercise` WRITE;
/*!40000 ALTER TABLE `exercise` DISABLE KEYS */;
INSERT INTO `exercise` VALUES (1,'Bench Press','Chest','Lie on a bench with feet flat on the ground. Grip the barbell slightly wider than shoulder-width. Lower the barbell to the chest and press upwards.',5.00,40),(2,'Squats','Legs','Stand with feet shoulder-width apart. Lower the body as if sitting back into a chair, keeping the back straight. Return to standing position.',7.00,50),(3,'Deadlift','Back','Stand with feet hip-width apart. Grip the barbell with hands just outside the knees. Lift the barbell while straightening the back and hips.',6.00,45),(4,'Jogging','Cardio','Maintain a steady running pace at a speed comfortable for long distances.',7.50,NULL),(5,'Push-ups','Chest','Start in a plank position with hands placed slightly wider than shoulder-width. Lower the body until the chest almost touches the ground and push back up.',4.00,30),(6,'Pull-ups','Back','Hang from a bar with an overhand grip. Pull the body up until the chin is above the bar, then lower back to the starting position.',8.00,25),(7,'Planks','Core','Hold a push-up position with the weight on the forearms, elbows bent 90 degrees. Maintain a straight line from head to heels.',3.80,NULL),(8,'Hammer Curls','Biceps','Stand with feet shoulder-width apart. Hold dumbbells at the sides with palms facing the body. Curl the weights up while keeping the upper arms stationary.',3.00,40),(9,'Leg Press','Legs','Sit on a leg press machine with feet on the platform. Press the platform away from the body by extending the legs.',4.50,35),(10,'Shoulder Press','Shoulders','Sit or stand with a barbell or dumbbells at shoulder height. Press the weight overhead until the arms are fully extended.',4.00,30),(11,'Lunges','Legs','Step forward with one leg, lowering the hips until both knees are bent at 90-degree angles. Push back to the starting position and repeat with the other leg.',6.00,50),(12,'Bicep Curls','Biceps','Stand with feet shoulder-width apart. Hold a barbell or dumbbells with an underhand grip. Curl the weight up while keeping the upper arms stationary.',3.50,35),(13,'Tricep Dips','Triceps','Sit on the edge of a bench with hands beside the hips. Slide off the bench and lower the body by bending the elbows, then push back up.',5.00,30),(14,'Crunches','Abs','Lie on the back with knees bent and feet flat on the floor. Lift the shoulders off the ground by engaging the abdominal muscles.',3.30,25),(15,'Running','Cardio','Maintain a steady running pace at a speed faster than jogging.',9.80,NULL),(16,'Lat Pulldown','Back','Sit at a lat pulldown machine. Grip the bar with hands slightly wider than shoulder-width. Pull the bar down to the chest, then return to the starting position.',5.00,35),(17,'Calf Raises','Calves','Stand with the balls of the feet on the edge of a step. Raise the heels as high as possible, then lower back down.',3.00,40),(18,'Chest Fly','Chest','Lie on a bench with dumbbells in each hand. With arms slightly bent, open the arms wide to the sides and then bring them back together over the chest.',4.00,45),(19,'Bent Over Rows','Back','Hold a barbell with an overhand grip. Bend at the hips and knees, keeping the back straight. Pull the barbell to the lower chest and return.',5.50,40),(20,'Seated Row','Back','Sit at a rowing machine with feet on the platform. Grip the handle with both hands and pull towards the torso, then extend the arms back out.',4.50,50),(21,'Leg Curl','Hamstrings','Lie face down on a leg curl machine with ankles under the padded lever. Curl the legs up towards the buttocks and lower back down.',4.00,40),(22,'Leg Extension','Quadriceps','Sit on a leg extension machine with feet under the padded lever. Extend the legs to lift the weight, then lower back down.',3.50,35),(23,'Mountain Climbers','Cardio','Start in a plank position. Bring one knee towards the chest, then switch legs in a running motion.',8.00,20),(24,'Russian Twists','Core','Sit on the ground with knees bent and feet slightly lifted. Hold a weight and twist the torso to move the weight from side to side.',3.80,40),(25,'Burpees','Cardio','From a standing position, drop into a squat with hands on the ground. Kick the feet back into a plank position, then jump back to squat and stand.',9.00,30),(26,'Bicycle Crunches','Abs','Lie on the back with hands behind the head. Bring one knee towards the chest while twisting the opposite elbow to touch it, then switch sides.',4.00,40),(27,'Overhead Tricep Extension','Triceps','Hold a dumbbell with both hands behind the head. Extend the arms to lift the weight overhead, then lower back down.',3.50,35),(28,'Side Planks','Core','Lie on one side with feet stacked. Prop up on one elbow and hold the body in a straight line from head to heels.',3.50,NULL),(29,'Treadmill Running','Cardio','Run on a treadmill at a consistent pace.',9.00,NULL),(30,'Elliptical Trainer','Cardio','Exercise on an elliptical trainer at a steady pace.',5.00,NULL),(32,'Goblet Squats','Legs','Hold a dumbbell or kettlebell close to the chest. Perform a squat while keeping the weight stable.',6.00,50),(33,'Step-Ups','Legs','Step onto a bench or platform with one leg, then bring the other leg up. Step back down and repeat with the opposite leg.',5.00,40),(34,'Hip Thrusts','Glutes','Sit on the ground with upper back against a bench. Place a barbell across the hips and thrust the hips upwards, then lower back down.',4.50,35),(35,'Side Lunges','Legs','Step to the side with one leg, bending the knee while keeping the other leg straight. Return to standing and repeat on the other side.',5.50,50),(36,'Face Pulls','Shoulders','Stand in front of a cable machine with a rope attachment. Pull the rope towards the face, keeping elbows high.',3.50,30);
/*!40000 ALTER TABLE `exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fitness_target`
--

DROP TABLE IF EXISTS `fitness_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fitness_target` (
  `user_id` int NOT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `body_fat_percentage` decimal(4,2) DEFAULT NULL,
  `daily_caloric_intake` int DEFAULT NULL,
  `daily_carb_intake_grams` int DEFAULT NULL,
  `daily_protein_intake_grams` int DEFAULT NULL,
  `daily_fat_intake_grams` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fitness_target_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fitness_target`
--

LOCK TABLES `fitness_target` WRITE;
/*!40000 ALTER TABLE `fitness_target` DISABLE KEYS */;
/*!40000 ALTER TABLE `fitness_target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meal`
--

DROP TABLE IF EXISTS `meal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meal` (
  `meal_id` int NOT NULL AUTO_INCREMENT,
  `creator_id` int NOT NULL,
  `recipe` text NOT NULL,
  `serving_size` decimal(5,2) DEFAULT NULL,
  `serving_unit` varchar(25) DEFAULT NULL,
  `calories_per_serving` int DEFAULT NULL,
  `carbs_per_serving` decimal(5,2) DEFAULT NULL,
  `protein_per_serving` decimal(5,2) DEFAULT NULL,
  `fat_per_serving` decimal(5,2) DEFAULT NULL,
  `public` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`meal_id`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `meal_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meal`
--

LOCK TABLES `meal` WRITE;
/*!40000 ALTER TABLE `meal` DISABLE KEYS */;
/*!40000 ALTER TABLE `meal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `program_id` int NOT NULL AUTO_INCREMENT,
  `creator_id` int NOT NULL,
  `program_name` varchar(35) NOT NULL,
  `focus` varchar(20) DEFAULT NULL,
  `description` text,
  `days_per_week` int NOT NULL,
  `public` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`program_id`),
  KEY `creator_id` (`creator_id`),
  CONSTRAINT `program_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `chk_focus` CHECK ((`focus` in (_utf8mb4'Full Body',_utf8mb4'Upper Body',_utf8mb4'Lower Body',_utf8mb4'Core',_utf8mb4'Chest',_utf8mb4'Back',_utf8mb4'Arms')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (1,1,'Push/Pull/Legs','Full Body',NULL,5,1),(2,2,'Push/Pull','Full Body',NULL,2,1),(3,1,'Core Blast','Core',NULL,5,0);
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_workout`
--

DROP TABLE IF EXISTS `program_workout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program_workout` (
  `program_id` int NOT NULL,
  `workout_id` int NOT NULL,
  `day_number` int NOT NULL,
  PRIMARY KEY (`program_id`,`workout_id`),
  KEY `workout_id` (`workout_id`),
  CONSTRAINT `program_workout_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`),
  CONSTRAINT `program_workout_ibfk_2` FOREIGN KEY (`workout_id`) REFERENCES `workout` (`workout_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_workout`
--

LOCK TABLES `program_workout` WRITE;
/*!40000 ALTER TABLE `program_workout` DISABLE KEYS */;
INSERT INTO `program_workout` VALUES (1,1,1),(1,2,2),(1,3,3),(2,1,1),(2,2,2);
/*!40000 ALTER TABLE `program_workout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `log_id` int NOT NULL,
  `workout_id` int DEFAULT NULL,
  `start_time` time NOT NULL,
  `duration_mins` int DEFAULT NULL,
  `cals_burned` int DEFAULT NULL,
  `weight_moved` decimal(10,2) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`session_id`),
  KEY `log_id` (`log_id`),
  KEY `workout_id` (`workout_id`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`log_id`) REFERENCES `daily_log` (`log_id`),
  CONSTRAINT `session_ibfk_2` FOREIGN KEY (`workout_id`) REFERENCES `workout` (`workout_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session_exercise`
--

DROP TABLE IF EXISTS `session_exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session_exercise` (
  `session_id` int NOT NULL,
  `exercise_id` int NOT NULL,
  `set_number` int NOT NULL,
  `reps` int NOT NULL,
  `weight` decimal(4,2) NOT NULL,
  PRIMARY KEY (`session_id`,`exercise_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `session_exercise_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `session` (`session_id`),
  CONSTRAINT `session_exercise_ibfk_2` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`exercise_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session_exercise`
--

LOCK TABLES `session_exercise` WRITE;
/*!40000 ALTER TABLE `session_exercise` DISABLE KEYS */;
/*!40000 ALTER TABLE `session_exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(35) NOT NULL,
  `password` varchar(18) NOT NULL,
  `current_program` int DEFAULT NULL,
  `first_name` varchar(35) NOT NULL,
  `last_name` varchar(35) NOT NULL,
  `height` decimal(5,2) NOT NULL,
  `weight` decimal(5,2) NOT NULL,
  `body_fat_percentage` decimal(4,2) DEFAULT NULL,
  `dob` date NOT NULL,
  `gender` varchar(35) DEFAULT NULL,
  `unit_type` enum('metric','imperial') NOT NULL DEFAULT 'metric',
  `profile_pic_path` varchar(50) NOT NULL DEFAULT 'profile_pics/default.jpg',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `user_ibfk_1` (`current_program`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`current_program`) REFERENCES `program` (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'jordo1','546389',NULL,'Jordan','Silver',6.00,178.00,18.80,'1999-08-12','Male','imperial','profile_pics/jordo1.jpeg'),(2,'thomas1','546389',NULL,'thomas','Ninh',6.00,170.00,NULL,'2014-08-07',NULL,'metric','profile_pics/default.jpg');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_public_programs`
--

DROP TABLE IF EXISTS `v_public_programs`;
/*!50001 DROP VIEW IF EXISTS `v_public_programs`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_public_programs` AS SELECT 
 1 AS `program_id`,
 1 AS `program_name`,
 1 AS `description`,
 1 AS `days_per_week`,
 1 AS `focus`,
 1 AS `creator_username`,
 1 AS `workouts`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `workout`
--

DROP TABLE IF EXISTS `workout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workout` (
  `workout_id` int NOT NULL AUTO_INCREMENT,
  `workout_name` varchar(35) NOT NULL,
  `approx_duration_mins` int DEFAULT NULL,
  PRIMARY KEY (`workout_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout`
--

LOCK TABLES `workout` WRITE;
/*!40000 ALTER TABLE `workout` DISABLE KEYS */;
INSERT INTO `workout` VALUES (1,'Chest & Triceps',75),(2,'Back & Biceps',75),(3,'Legs',60);
/*!40000 ALTER TABLE `workout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workout_exercise`
--

DROP TABLE IF EXISTS `workout_exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workout_exercise` (
  `workout_id` int NOT NULL,
  `exercise_id` int NOT NULL,
  `set_number` int NOT NULL,
  `reps` int NOT NULL,
  PRIMARY KEY (`workout_id`,`exercise_id`),
  KEY `exercise_id` (`exercise_id`),
  CONSTRAINT `workout_exercise_ibfk_1` FOREIGN KEY (`workout_id`) REFERENCES `workout` (`workout_id`),
  CONSTRAINT `workout_exercise_ibfk_2` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`exercise_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout_exercise`
--

LOCK TABLES `workout_exercise` WRITE;
/*!40000 ALTER TABLE `workout_exercise` DISABLE KEYS */;
/*!40000 ALTER TABLE `workout_exercise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `v_public_programs`
--

/*!50001 DROP VIEW IF EXISTS `v_public_programs`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_public_programs` AS select `p`.`program_id` AS `program_id`,`p`.`program_name` AS `program_name`,`p`.`description` AS `description`,`p`.`days_per_week` AS `days_per_week`,`p`.`focus` AS `focus`,(select `u`.`username` from `user` `u` where (`u`.`user_id` = `p`.`creator_id`)) AS `creator_username`,(select json_arrayagg(json_object('workout_id',`w`.`workout_id`,'workout_name',`w`.`workout_name`,'day_number',`pw`.`day_number`,'approx_duration',`w`.`approx_duration_mins`)) from (`program_workout` `pw` join `workout` `w` on((`pw`.`workout_id` = `w`.`workout_id`))) where (`pw`.`program_id` = `p`.`program_id`)) AS `workouts` from `program` `p` where (`p`.`public` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-27  3:51:59
