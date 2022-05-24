-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2022 at 05:14 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.14

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
(0, 100, '20:04:08', '2022-05-23'),
(1, 50, '20:04:08', '2022-05-24');

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
(11, 11, '8dfa090ee069a9b36fad8e273845a0b9495eb631337190a7f97c931ba4ccebe7');

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
(0, 0, '20:04:08', '2022-05-23'),
(0, 0, '20:41:09', '2022-05-24'),
(1, 1, '20:04:08', '2022-05-24'),
(2, 0, '20:41:09', '2022-05-24'),
(3, 0, '20:41:09', '2022-05-24'),
(4, 0, '20:41:09', '2022-05-24'),
(5, 0, '20:41:09', '2022-05-24'),
(6, 0, '20:41:09', '2022-05-24'),
(7, 0, '20:41:09', '2022-05-24'),
(8, 0, '20:41:09', '2022-05-24'),
(9, 0, '20:41:09', '2022-05-24'),
(10, 0, '20:41:09', '2022-05-24');

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
(1, 'admin', 'admin', 'A', '2022-03-30 07:06:41'),
(12, 'admin', 'admin@123', 'A', '2022-04-01 06:13:26'),
(14, 'sample', 'sample123', 'S', '2022-04-01 07:02:59'),
(15, 'teacher', 'teacher', 'T', '2022-04-16 11:31:06');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
