-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 31, 2019 at 08:14 AM
-- Server version: 10.3.16-MariaDB
-- PHP Version: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `billing`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` bigint(20) UNSIGNED NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `state` varchar(30) NOT NULL,
  `city` varchar(30) DEFAULT NULL,
  `gst_number` varchar(50) DEFAULT NULL,
  `addhar_card_number` varchar(50) DEFAULT NULL,
  `pan_number` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `address`, `state`, `city`, `gst_number`, `addhar_card_number`, `pan_number`, `phone_number`) VALUES
(1, 'gursimar', 'kaur', 'sth', 'Punjab', 'ludhiana', '', '8575 2562 2452', 'JMXPS4639F', '9878717057'),
(3, 'sameer', 'sharma', 'sfa', 'Punjab', 'ldh', '', '1234 5678 9101', '', '8837833685'),
(4, 'anand ', 'kumar', 'DMC', 'Punjab', 'ludhiana', '', '9807 4321 1201', 'JMXPS4639F', '9876543210'),
(5, 'alice', 'game', 'idk', 'Punjab', 'jaipur', '', '1234 6547 9999', '', '8837833621'),
(6, 'sharukh', 'khan', 'idk', 'Maharashtra', 'mumbai', '', '9876 5432 1111', '', '9779478333');

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_id` varchar(100) DEFAULT NULL,
  `item_name` varchar(200) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `gst_per` varchar(50) NOT NULL,
  `hsn_code` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_id`, `item_name`, `price`, `gst_per`, `hsn_code`) VALUES
('21', 'jeans', '500', '5', '');

-- --------------------------------------------------------

--
-- Table structure for table `passwords`
--

CREATE TABLE `passwords` (
  `hash` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `salt` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `passwords`
--

INSERT INTO `passwords` (`hash`, `salt`) VALUES
('3c8e6aa9db2730c68facff3a9a943983438393b38a66663f833dbb40b6e59004a7d339e7122e19db3bee538dbdaec7115fcc070dbced961be94873bf263a8de4', '831e7eb6ff4e4ed98ecc254e0de8afda');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
