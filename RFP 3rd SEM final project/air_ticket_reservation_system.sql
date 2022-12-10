

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `air_ticket_reservation_system`
--
Database:'data'
-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` varchar(20) NOT NULL,
  `seats` decimal(4,0) DEFAULT NULL,
  PRIMARY KEY (`airline_name`,`airplane_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('China Eastern', 'B-1234', '60'),
('China Eastern', 'B-1077', '90'),
('China Eastern', 'B-2002', '120'),
('China Eastern', 'A-2451', '3'),
('China Eastern', 'A-2313', '4'),
('China Eastern', 'B-1123', '20'),
('China Eastern', 'B-1948', '2'),
('China Eastern', 'B-1111', '5'),
('China Eastern', 'B-2222', '10'),
('China Eastern', 'C-1122', '15'),
('China Eastern', 'C-2222', '10');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `airport_code` char(3) NOT NULL,
  `airport_name` varchar(100) DEFAULT NULL,
  `airport_city` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`airport_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_code`, `airport_name`, `airport_city`) VALUES
('JFK', 'John F. Kennedy International Airport', 'NYC'),
('PVG', 'Shanghai Pudong International Airport', 'Shanghai'),
('ATL', 'Hartsfield-Jackson International Airport', 'GA'),
('SIN', 'Singapore Changi Airport', 'Changi'),
('HKG', 'Hong Kong International Airport', 'Hongkong'),
('ABC', 'Test Airport', 'Test City'),
('SSS', 'test2', 'test2');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email` varchar(100) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_password` varchar(255) DEFAULT NULL,
  `building_number` varchar(10) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `customer_name`, `customer_password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('user1@gmail.com', 'Steven', '482c811da5d5b4bc6d497ffa98491e38', '101', 'Johnson St', 'Brooklyn', 'NY', '9293344454', 'EA23842', '2022-07-25', 'US', '1990-01-02'),
('user2@gmail.com', 'Jack', '8279309a6fa82723da732043c3620f81', '102', 'Prospect St', 'San Francisco', 'CA', '9493343454', 'EA23242', '2023-07-26', 'US', '1990-04-02'),
('user3@gmail.com', 'Jin', 'b3ed48555a989b8ee27f613f7b5724dd', '45', 'Wanyuan St', 'Hongqiao', 'Shanghai', '9493366666', 'EA55242', '2024-07-16', 'China', '1970-04-22'),
('user4@gmail.com', 'Kevin', '60a7e954fde05b08d26269b6cab13f4b', '16', '​​Sandilands Road', 'null ', ' null', '123948239', 'EA92384', '2019-02-07', 'Singapore', '1999-11-02'),
('user5@gmail.com', 'Renee', '208969c79d95a090067e6f448cf2749c', '111', '​​Sandilands Road', 'null', 'null', '234394734', 'EA23242', '2020-07-26', 'US', '2004-04-02'),
('user6@gmail.com', 'Ken', 'deff6aa31b45aec5682b232fc7d82928', '2', ' Peachtree Street', 'Atlanta', 'GA', '6827499538', 'MU34827', '2024-07-16', 'US', '1988-09-03'),
('yw3602@nyu.edu', 'Yilun Wu', '1e269908610ead310d5d785024d18985', '100', 'Willoughby', 'Brooklyn', 'NY', '6466660000', 'E800000', '2025-06-27', 'China', '1998-10-23');

-- --------------------------------------------------------

--
-- Table structure for table `customerrate`
--

DROP TABLE IF EXISTS `customerrate`;
CREATE TABLE IF NOT EXISTS `customerrate` (
  `email` varchar(100) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_datetime` timestamp NOT NULL,
  `rate` decimal(2,0) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`email`,`airline_name`,`flight_number`,`departure_datetime`),
  KEY `airline_name` (`airline_name`),
  KEY `flight_number` (`flight_number`),
  KEY `departure_datetime` (`departure_datetime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customerrate`
--

INSERT INTO `customerrate` (`email`, `airline_name`, `flight_number`, `departure_datetime`, `rate`, `comments`) VALUES
('user1@gmail.com', 'China Eastern', 'CPA2321', '2021-10-18 16:00:30', '3', 'Safe flight'),
('user2@gmail.com', 'China Eastern', 'DL6388', '2020-03-13 13:00:30', '4', ''),
('user4@gmail.com', 'China Eastern', 'DL6388', '2021-12-03 16:00:30', '5', ''),
('user2@gmail.com', 'China Eastern', 'MU588', '2021-09-18 16:00:30', '5', 'Good and safe');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_datetime` timestamp NOT NULL,
  `departure_airport` char(3) DEFAULT NULL,
  `arrival_datetime` timestamp NULL DEFAULT NULL,
  `arrival_airport` char(3) DEFAULT NULL,
  `base_price` decimal(10,2) DEFAULT NULL,
  `airplane_id` varchar(20) DEFAULT NULL,
  `flight_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`airline_name`,`flight_number`,`departure_datetime`),
  KEY `departure_airport` (`departure_airport`),
  KEY `arrival_airport` (`arrival_airport`),
  KEY `airplane_id` (`airplane_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_datetime`, `departure_airport`, `arrival_datetime`, `arrival_airport`, `base_price`, `airplane_id`, `flight_status`) VALUES
('China Eastern', 'DL6388', '2020-03-13 13:00:30', 'PVG', '2020-03-13 23:00:30', 'JFK', '5000.00', 'B-2002', 'on-time'),
('China Eastern', 'MU588', '2021-09-18 16:00:30', 'JFK', '2021-09-19 07:00:30', 'PVG', '6000.00', 'B-1077', 'delayed'),
('China Eastern', 'DL6388', '2023-03-13 13:00:30', 'PVG', '2023-03-13 23:00:30', 'JFK', '5000.00', 'B-2002', 'delayed'),
('China Eastern', 'AA2395', '2020-12-31 15:00:30', 'PVG', '2020-12-31 15:00:30', 'ATL', '5000.50', 'A-2567', 'delayed'),
('China Eastern', 'SA1001', '2020-01-01 23:10:30', 'PVG', '2020-01-02 09:25:00', 'JFK', '5300.50', 'B-4291', 'on-time'),
('China Eastern', 'CPA2321', '2021-10-18 16:00:30', 'HKG', '2021-10-19 07:00:30', 'PVG', '7777.00', 'B-2222', 'on-time'),
('China Eastern', 'AB1234', '2023-12-25 13:30:00', 'JFK', '2023-12-26 06:20:00', 'PVG', '5500.00', 'A-2313', 'on-time'),
('China Eastern', 'AB122021', '2021-12-20 15:00:00', 'PVG', '2021-12-21 15:00:00', 'JFK', '4510.00', 'B-1111', 'delayed'),
('China Eastern', 'AB010122', '2022-01-01 15:00:00', 'JFK', '2022-01-02 15:00:00', 'PVG', '4500.00', 'B-1111', 'on-time');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
CREATE TABLE IF NOT EXISTS `purchase` (
  `ticket_id` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `sold_price` decimal(10,2) DEFAULT NULL,
  `card_type` varchar(20) DEFAULT NULL,
  `card_number` varchar(20) DEFAULT NULL,
  `name_on_card` varchar(100) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `purchase_datetime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`ticket_id`, `email`, `sold_price`, `card_type`, `card_number`, `name_on_card`, `expiration_date`, `purchase_datetime`) VALUES
('B345323', 'user3@gmail.com', '6000.00', 'Visa', '1231928742492', 'Jin', '2021-09-30', '2020-05-30 11:05:23'),
('A123124', 'user2@gmail.com', '5000.00', 'Visa', '9253228759492', 'Jack', '2024-05-02', '2019-09-03 16:05:23'),
('B222222', 'user1@gmail.com', '6000.00', 'Visa', '1231928742492', 'Steven', '2021-09-30', '2020-05-30 11:05:23'),
('A111111', 'user2@gmail.com', '5000.00', 'Visa', '9253228759492', 'Jack', '2024-05-02', '2019-09-03 16:05:23'),
('1ChinaEasternAB123420231225133000', 'user2@gmail.com', '5500.00', 'Visa', '9253228759492', 'Jack', '2024-05-02', '2021-10-10 14:15:00'),
('2ChinaEasternAB123420231225133000', 'yw3602@nyu.edu', '5500.00', 'Visa', '1234123412341234', 'Yilun', '2025-05-05', '2021-11-12 15:15:00'),
('3ChinaEasternAB123420231225133000', 'user2@gmail.com', '5500.00', 'Visa', '1234432112344321', 'JackCard2', '2024-01-01', '2021-12-05 05:38:53');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `username` varchar(50) NOT NULL,
  `userpassword` varchar(255) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `airline_name` (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`username`, `userpassword`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('staff0001', 'e10adc3949ba59abbe56e057f20f883e', 'Ming', 'Li', '1984-03-02', 'China Eastern'),
('staff0002', 'e10adc3949ba59abbe56e057f20f883e', 'Wei', 'Chen', '1986-03-04', 'China Eastern'),
('Thisisanotherstaff', 'e10adc3949ba59abbe56e057f20f883e', 'Helen', 'Eva', '1999-02-10', 'China Eastern'),
('ylwu', '1e269908610ead310d5d785024d18985', 'Yilun', 'Wu', '1998-10-23', 'China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `staffphone`
--

DROP TABLE IF EXISTS `staffphone`;
CREATE TABLE IF NOT EXISTS `staffphone` (
  `username` varchar(50) DEFAULT NULL,
  `phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`phone_number`),
  KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staffphone`
--

INSERT INTO `staffphone` (`username`, `phone_number`) VALUES
('staff0001', '1328974359234'),
('staff0001', '213874928423'),
('staff0002', '184727483'),
('staff0002', '934729438'),
('Thisisanotherstaff', '24459038'),
('ylwu', '6466669999'),
('ylwu', '1112223333');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `ticket_id` varchar(100) NOT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `flight_number` varchar(20) DEFAULT NULL,
  `departure_datetime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `airline_name` (`airline_name`),
  KEY `flight_number` (`flight_number`),
  KEY `departure_datetime` (`departure_datetime`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_number`, `departure_datetime`) VALUES
('B345323', 'China Eastern', 'MU588', '2021-09-18 16:00:30'),
('A123124', 'China Eastern', 'DL6388', '2020-03-13 13:00:30'),
('A111111', 'China Eastern', 'MU588', '2021-09-18 16:00:30'),
('A111112', 'China Eastern', 'MU588', '2021-09-18 16:00:30'),
('B222222', 'China Eastern', 'CPA2321', '2021-10-18 16:00:30'),
('B123332', 'China Eastern', 'SA1001', '2022-01-01 23:10:30'),
('B123311', 'China Eastern', 'AA2349', '2021-09-18 16:00:30'),
('1ChinaEasternAB123420231225133000', 'China Eastern', 'AB1234', '2023-12-25 13:30:00'),
('2ChinaEasternAB123420231225133000', 'China Eastern', 'AB1234', '2023-12-25 13:30:00'),
('3ChinaEasternAB123420231225133000', 'China Eastern', 'AB1234', '2023-12-25 13:30:00'),
('4ChinaEasternAB123420231225133000', 'China Eastern', 'AB1234', '2023-12-25 13:30:00'),
('1ChinaEasternAB010122202201011000', 'China Eastern', 'AB010122', '2022-01-01 15:00:00'),
('2ChinaEasternAB010122202201011000', 'China Eastern', 'AB010122', '2022-01-01 15:00:00'),
('3ChinaEasternAB010122202201011000', 'China Eastern', 'AB010122', '2022-01-01 15:00:00'),
('4ChinaEasternAB010122202201011000', 'China Eastern', 'AB010122', '2022-01-01 15:00:00'),
('5ChinaEasternAB010122202201011000', 'China Eastern', 'AB010122', '2022-01-01 15:00:00'),
('1ChinaEasternAB122021202112201000', 'China Eastern', 'AB122021', '2021-12-20 15:00:00'),
('2ChinaEasternAB122021202112201000', 'China Eastern', 'AB122021', '2021-12-20 15:00:00'),
('3ChinaEasternAB122021202112201000', 'China Eastern', 'AB122021', '2021-12-20 15:00:00'),
('4ChinaEasternAB122021202112201000', 'China Eastern', 'AB122021', '2021-12-20 15:00:00'),
('5ChinaEasternAB122021202112201000', 'China Eastern', 'AB122021', '2021-12-20 15:00:00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
