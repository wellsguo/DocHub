/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80017
 Source Host           : localhost:3306
 Source Schema         : stu

 Target Server Type    : MySQL
 Target Server Version : 80017
 File Encoding         : 65001

 Date: 28/10/2019 08:49:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `id` char(3) COLLATE utf8_bin NOT NULL,
  `name` varchar(30) COLLATE utf8_bin NOT NULL,
  `school_hour` smallint(6) DEFAULT NULL,
  `credit` decimal(3,1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of course
-- ----------------------------
BEGIN;
INSERT INTO `course` VALUES ('A01', 'C++', 40, 4.0);
INSERT INTO `course` VALUES ('A02', 'Data Structure', 40, 4.0);
INSERT INTO `course` VALUES ('A03', 'Algorithm', 60, 4.0);
COMMIT;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `id` char(9) COLLATE utf8_bin NOT NULL,
  `name` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `class` char(20) COLLATE utf8_bin DEFAULT NULL,
  `gender` char(1) COLLATE utf8_bin DEFAULT NULL,
  `birthday` datetime DEFAULT NULL,
  `phone` char(11) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `remark` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of student
-- ----------------------------
BEGIN;
INSERT INTO `student` VALUES ('100100100', 'Adams', '078013', '2', '1996-04-18 00:00:00', '6795911', '37033033@gmail.com', '');
INSERT INTO `student` VALUES ('100100101', 'Zoe', '078013', '1', '1995-09-09 00:00:00', '5453232', 'zoe@gmail.com', NULL);
COMMIT;

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course` (
  `student_id` char(9) COLLATE utf8_bin NOT NULL,
  `course_id` char(3) COLLATE utf8_bin NOT NULL,
  `achievement` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`student_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of student_course
-- ----------------------------
BEGIN;
INSERT INTO `student_course` VALUES ('100100100', 'A01', 90, '2019-10-10 00:00:00');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;











(1)
mysql> upate student_course set course_id='A04' where student_id=`100100100`;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'upate student_course set course_id='A04' where student_id=`100100100`' at line 1

(2)


-- declare
CREATE DEFINER=`root`@`localhost` PROCEDURE `COUNT_MORE_THAN`(in in_course_id char(3), in in_score int, out count int)
BEGIN
  SELECT
		count(*) into @count
	FROM
		course
		LEFT JOIN student_course ON course.id = student_course.course_id 
	WHERE
		id = in_course_id 
		AND achievement >= in_score;

  SET count = @count;

END


-- call
set @in_course_id='A01';
set @in_score=90;
set @count=0;


call COUNT_MORE_THAN(@in_course_id, @in_score, @count);
select @count;


(3)

-- add 10000000 records




-- before
set profiling = 1;

select * from student where id = '100100901';

show profiles;


-- after
ALTER TABLE `student` ADD INDEX index_id( `id` ); 

select * from student where id = '100100901';

show profiles;

