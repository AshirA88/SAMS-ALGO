-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2022 at 10:55 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sams`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `rollno` int(16) DEFAULT NULL,
  `accuracy` int(16) DEFAULT NULL,
  `timestamp` time DEFAULT current_timestamp(),
  `date` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`rollno`, `accuracy`, `timestamp`, `date`) VALUES
(0, 73, '20:52:10', '2022-05-26'),
(1, 187, '20:52:49', '2022-05-26'),
(2, 125, '20:57:52', '2022-05-26'),
(5, 133, '20:58:32', '2022-05-26'),
(0, 106, '19:23:02', '2022-05-27'),
(1, 138, '19:24:15', '2022-05-27'),
(2, 102, '19:25:06', '2022-05-27'),
(3, 147, '19:25:42', '2022-05-27'),
(4, 103, '19:26:37', '2022-05-27'),
(5, 255, '19:27:24', '2022-05-27'),
(6, 217, '19:28:20', '2022-05-27'),
(7, 156, '19:28:48', '2022-05-27'),
(8, 271, '19:30:00', '2022-05-27'),
(9, 147, '19:30:40', '2022-05-27');

-- --------------------------------------------------------

--
-- Table structure for table `fpstore`
--

CREATE TABLE `fpstore` (
  `roll` int(100) DEFAULT NULL,
  `id` int(100) DEFAULT NULL,
  `hash` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fpstore`
--

INSERT INTO `fpstore` (`roll`, `id`, `hash`) VALUES
(0, 0, '0608081cb1732ff1e0f6f35e5e8e60214607a77c793402ca623b828f4b1095f6'),
(1, 1, 'ef955f4f0f80d00ef03e81ad14f7df72a98945d8dd4b8558ed0e14b0fdfa7187'),
(2, 2, 'b318c924af194f59077917ec87ee38cdf41010874a23ff4a20e73ed663aa4944'),
(3, 3, '2c49a0a42a1480cc20a3f91cb316c280667e6a294196169d881c78f5b79affd7'),
(4, 4, '2faf295ab9ba66aea1811e31deac1c663d579f4ca7dc5dfe8479def462311625'),
(5, 5, 'bdba738f8d768eaba3aba571ff20b0e375a0cb9972b9b8979b88fc2ae192c8d8'),
(6, 6, '343093f1a835bacb719845abdbe9822590d24c9f2ecc215cb280bf7b6e128080'),
(7, 7, 'd51dee7099449dbe54ed6f339c8126a804ec90f53ff07a73d2bf2b2d5002f9f1'),
(8, 8, '978b76690f626af16b7729a3f8afffd2fc19a4d48774e483139bd3c386929ef5'),
(9, 9, '056c2db65e8a5016a8e4163dd9b70b1f39d7ef86059d9b27c5ce6397f7246bd1');

-- --------------------------------------------------------

--
-- Table structure for table `record`
--

CREATE TABLE `record` (
  `id` int(255) DEFAULT NULL,
  `attendee` int(255) DEFAULT NULL,
  `timestamp` time DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `record`
--

INSERT INTO `record` (`id`, `attendee`, `timestamp`, `date`) VALUES
(1, 1, '20:52:49', '2022-05-26'),
(2, 1, '20:57:52', '2022-05-26'),
(3, 0, '21:01:45', '2022-05-26'),
(4, 0, '21:01:45', '2022-05-26'),
(5, 1, '20:58:32', '2022-05-26'),
(6, 0, '21:01:45', '2022-05-26'),
(7, 0, '21:01:45', '2022-05-26'),
(8, 0, '21:01:45', '2022-05-26'),
(9, 0, '21:01:45', '2022-05-26'),
(0, 1, '19:23:02', '2022-05-27'),
(1, 1, '19:24:15', '2022-05-27'),
(2, 1, '19:25:06', '2022-05-27'),
(3, 1, '19:25:42', '2022-05-27'),
(4, 1, '19:26:37', '2022-05-27'),
(5, 1, '19:27:24', '2022-05-27'),
(6, 1, '19:28:20', '2022-05-27'),
(7, 1, '19:28:48', '2022-05-27'),
(8, 1, '19:30:00', '2022-05-27'),
(9, 1, '19:30:40', '2022-05-27');

-- --------------------------------------------------------

--
-- Table structure for table `total`
--

CREATE TABLE `total` (
  `id` int(255) DEFAULT NULL,
  `total_count` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `total`
--

INSERT INTO `total` (`id`, `total_count`) VALUES
(1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `UserName` varchar(100) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `UserType` varchar(10) DEFAULT NULL,
  `TimeOfCreation` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `UserName`, `Password`, `UserType`, `TimeOfCreation`) VALUES
(0, 'teacher', 'teacher', 'T', '2022-04-16 11:31:06'),
(1, 'atharva', 'atharva', 'S', '2022-04-01 07:02:59'),
(2, 'ashir', 'ashir', 'S', '2022-05-27 19:40:58'),
(98, 'admin', 'admin@123', 'A', '2022-04-01 06:13:26'),
(99, 'admin', 'admin', 'A', '2022-03-30 07:06:41');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
