-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 29, 2024 at 01:51 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mede`
--

-- --------------------------------------------------------

--
-- Table structure for table `authentication_userprofile`
--

CREATE TABLE `authentication_userprofile` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `dob` date DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `user_type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `authentication_userprofile`
--

INSERT INTO `authentication_userprofile` (`id`, `password`, `last_login`, `is_superuser`, `phone_number`, `first_name`, `last_name`, `dob`, `email`, `address`, `is_active`, `is_staff`, `gender`, `user_type`) VALUES
(1, 'pbkdf2_sha256$600000$JD12Wg4KEmp9iFR4UHHS5k$kDmG0ZnE/s7GrfSQZ/qSjiOtFOEolRKv/JsX4F9cuiM=', '2024-02-29 12:47:25.727563', 1, '+88001955112789', 'Jubayerrrrrrrrr', 'Hossaainnnnnnnnn', '2023-10-13', 'jub@gmail.com', 'West masdairdddd', 1, 1, 'M', 'days'),
(5, 'pbkdf2_sha256$600000$K3Hnccf6QK1uCuq5fKZlOy$RWoecJlu0osdOQiE4RI3DSGDBx+Z60v8FlD4HTa3ZME=', '2023-11-15 17:54:25.000000', 0, '+88001841552789', 'Jubayerrrrrrrrr', 'Hossainnnnnnnn', '2023-10-13', 'jubayer@gmail.com', 'narayanganj', 1, 1, 'M', 'quantity');

-- --------------------------------------------------------

--
-- Table structure for table `authentication_userprofile_groups`
--

CREATE TABLE `authentication_userprofile_groups` (
  `id` bigint(20) NOT NULL,
  `userprofile_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authentication_userprofile_user_permissions`
--

CREATE TABLE `authentication_userprofile_user_permissions` (
  `id` bigint(20) NOT NULL,
  `userprofile_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `authentication_userprofile_user_permissions`
--

INSERT INTO `authentication_userprofile_user_permissions` (`id`, `userprofile_id`, `permission_id`) VALUES
(1, 5, 43),
(2, 5, 45);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add product', 6, 'add_product'),
(22, 'Can change product', 6, 'change_product'),
(23, 'Can delete product', 6, 'delete_product'),
(24, 'Can view product', 6, 'view_product'),
(25, 'Can add main_product', 7, 'add_main_product'),
(26, 'Can change main_product', 7, 'change_main_product'),
(27, 'Can delete main_product', 7, 'delete_main_product'),
(28, 'Can view main_product', 7, 'view_main_product'),
(29, 'Can add user profile', 8, 'add_userprofile'),
(30, 'Can change user profile', 8, 'change_userprofile'),
(31, 'Can delete user profile', 8, 'delete_userprofile'),
(32, 'Can view user profile', 8, 'view_userprofile'),
(33, 'Can change own user profile', 8, 'change_own_userprofile'),
(34, 'Can add orders', 9, 'add_orders'),
(35, 'Can change orders', 9, 'change_orders'),
(36, 'Can delete orders', 9, 'delete_orders'),
(37, 'Can view orders', 9, 'view_orders'),
(38, 'Can add profile_ med list', 10, 'add_profile_medlist'),
(39, 'Can change profile_ med list', 10, 'change_profile_medlist'),
(40, 'Can delete profile_ med list', 10, 'delete_profile_medlist'),
(41, 'Can view profile_ med list', 10, 'view_profile_medlist'),
(42, 'Can add presciption_order', 11, 'add_presciption_order'),
(43, 'Can change presciption_order', 11, 'change_presciption_order'),
(44, 'Can delete presciption_order', 11, 'delete_presciption_order'),
(45, 'Can view presciption_order', 11, 'view_presciption_order');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2023-10-11 20:59:52.623120', '5', '+88001841552789', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Dob\", \"Email\", \"Address\"]}}]', 8, 1),
(2, '2023-10-16 18:42:45.785421', '5', '+88001841552789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(3, '2023-10-16 18:42:54.447163', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(4, '2023-10-16 22:06:26.240069', '1', 'Napa', 1, '[{\"added\": {}}]', 7, 1),
(5, '2023-10-17 05:56:32.422473', '2', 'Monteen', 1, '[{\"added\": {}}]', 7, 1),
(6, '2023-10-17 05:57:09.085444', '2', 'Monteen', 2, '[{\"changed\": {\"fields\": [\"Feature\"]}}]', 7, 1),
(7, '2023-10-17 16:01:25.543645', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(8, '2023-10-17 16:02:03.457126', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(9, '2023-10-17 16:37:18.293966', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(10, '2023-10-17 16:37:32.989119', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(11, '2023-10-17 16:37:57.709112', '1', '+88001955112789', 2, '[]', 8, 1),
(12, '2023-10-17 16:38:14.615602', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(13, '2023-10-17 16:38:34.973049', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(14, '2023-10-17 16:39:20.371554', '1', '+88001955112789', 2, '[]', 8, 1),
(15, '2023-10-17 16:42:06.428164', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(16, '2023-10-17 18:56:56.824211', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(17, '2023-10-17 18:57:55.444561', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(18, '2023-10-17 18:58:21.248151', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(19, '2023-10-17 19:18:13.547407', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(20, '2023-10-17 19:20:59.237193', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(21, '2023-10-17 19:22:39.560121', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(22, '2023-10-17 19:22:44.231983', '1', '+88001955112789', 2, '[]', 8, 1),
(23, '2023-10-17 19:57:27.401291', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(24, '2023-10-17 20:05:07.250671', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(25, '2023-10-17 20:10:25.215157', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(26, '2023-10-17 20:11:37.794228', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(27, '2023-10-17 20:40:43.583645', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(28, '2023-10-20 05:06:50.196273', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(29, '2023-10-20 05:09:14.155223', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(30, '2023-10-20 05:09:44.514208', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(31, '2023-10-20 05:14:31.818698', '1', 'Napa', 2, '[{\"changed\": {\"fields\": [\"Feature\"]}}]', 7, 1),
(32, '2023-10-20 05:14:50.346472', '1', 'Napa', 2, '[{\"changed\": {\"fields\": [\"Feature\"]}}]', 7, 1),
(33, '2023-10-20 06:04:02.056892', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(34, '2023-10-20 06:05:19.181234', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(35, '2023-10-24 14:29:19.758629', '3', 'Orders object (3)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 9, 1),
(36, '2023-10-24 14:29:54.849986', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(37, '2023-10-24 14:31:33.379434', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(38, '2023-10-24 20:20:43.915817', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(39, '2023-10-24 20:43:02.703449', '3', 'orsaline', 1, '[{\"added\": {}}]', 7, 1),
(40, '2023-11-05 17:48:49.874807', '10', 'Orders object (10)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 9, 1),
(41, '2023-11-05 17:58:04.441469', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(42, '2023-11-08 11:46:48.114324', '1', '+88001955112789', 2, '[{\"changed\": {\"fields\": [\"User type\"]}}]', 8, 1),
(43, '2023-11-13 18:22:00.141949', '3', 'orsaline', 2, '[{\"changed\": {\"fields\": [\"Otc status\"]}}]', 7, 1),
(44, '2023-11-14 11:50:57.524453', '1', 'Napa', 2, '[{\"changed\": {\"fields\": [\"Otc status\"]}}]', 7, 1),
(45, '2023-11-14 12:08:49.836925', '5', '+88001841552789', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 8, 1),
(46, '2023-11-14 12:10:29.918587', '5', '+88001841552789', 2, '[{\"changed\": {\"fields\": [\"Is staff\"]}}]', 8, 1),
(47, '2023-11-15 17:53:52.755504', '7', 'presciption_order object (7)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 11, 5),
(48, '2023-11-15 18:24:56.782771', '5', '+88001841552789', 2, '[]', 8, 1),
(49, '2023-11-15 18:33:59.432649', '45', 'Orders object (45)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 9, 1),
(50, '2023-11-18 09:54:25.465395', '46', 'Orders object (46)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 9, 1),
(51, '2023-11-18 09:54:34.955657', '46', 'Orders object (46)', 2, '[{\"changed\": {\"fields\": [\"Delivery status\"]}}]', 9, 1),
(52, '2023-11-18 09:55:17.214142', '6', 'presciption_order object (6)', 2, '[{\"changed\": {\"fields\": [\"Del adress\", \"Delivery status\"]}}]', 11, 1),
(53, '2023-11-18 09:57:59.382857', '45', 'Orders object (45)', 2, '[{\"changed\": {\"fields\": [\"Status\"]}}]', 9, 1),
(54, '2023-11-18 09:58:18.838180', '45', 'Orders object (45)', 2, '[{\"changed\": {\"fields\": [\"Delivery status\"]}}]', 9, 1),
(55, '2023-11-18 09:58:24.878785', '44', 'Orders object (44)', 2, '[{\"changed\": {\"fields\": [\"Status\", \"Delivery status\"]}}]', 9, 1),
(56, '2023-11-18 09:58:33.675237', '43', 'Orders object (43)', 2, '[{\"changed\": {\"fields\": [\"Status\", \"Delivery status\"]}}]', 9, 1),
(57, '2024-02-29 12:48:31.890435', '3', 'orsaline', 2, '[{\"changed\": {\"fields\": [\"Otc status\"]}}]', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(8, 'authentication', 'userprofile'),
(4, 'contenttypes', 'contenttype'),
(6, 'Home', 'product'),
(7, 'products', 'main_product'),
(9, 'products', 'orders'),
(11, 'products', 'presciption_order'),
(10, 'products', 'profile_medlist'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-10-11 20:52:39.487942'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-10-11 20:52:39.527048'),
(3, 'auth', '0001_initial', '2023-10-11 20:52:39.669438'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-10-11 20:52:39.680255'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-10-11 20:52:39.683457'),
(6, 'auth', '0004_alter_user_username_opts', '2023-10-11 20:52:39.691653'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-10-11 20:52:39.691653'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-10-11 20:52:39.701377'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-10-11 20:52:39.701377'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-10-11 20:52:39.708015'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-10-11 20:52:39.716433'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-10-11 20:52:39.724664'),
(13, 'auth', '0011_update_proxy_permissions', '2023-10-11 20:52:39.738249'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-10-11 20:52:39.740918'),
(15, 'authentication', '0001_initial', '2023-10-11 20:52:39.897389'),
(16, 'admin', '0001_initial', '2023-10-11 20:52:39.963401'),
(17, 'admin', '0002_logentry_remove_auto_add', '2023-10-11 20:52:39.971645'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-10-11 20:52:39.979736'),
(19, 'sessions', '0001_initial', '2023-10-11 20:52:40.004248'),
(20, 'authentication', '0002_alter_userprofile_email', '2023-10-11 20:57:50.941715'),
(21, 'authentication', '0003_userprofile_gender', '2023-10-11 21:12:54.970588'),
(22, 'authentication', '0004_userprofile_user_type', '2023-10-16 18:40:20.175142'),
(23, 'authentication', '0005_alter_userprofile_user_type', '2023-10-16 18:40:20.183225'),
(24, 'authentication', '0006_alter_userprofile_user_type', '2023-10-16 21:59:44.815641'),
(26, 'authentication', '0007_alter_userprofile_user_type', '2023-10-17 15:39:19.513300'),
(27, 'products', '0002_rename_pieceperstrip_main_product_medperstrip', '2023-10-17 16:48:11.178920'),
(28, 'products', '0002_profile_medlist', '2023-10-24 14:26:31.815803'),
(29, 'products', '0003_orders_timestamp', '2023-10-24 14:26:31.844361'),
(30, 'products', '0004_orders_status', '2023-10-24 14:26:31.873579'),
(31, 'products', '0005_alter_orders_status', '2023-10-24 14:26:31.882104'),
(32, 'products', '0006_main_product_otc_status', '2023-11-13 18:21:11.072965'),
(33, 'products', '0007_orders_prescriptions', '2023-11-13 20:26:41.787637'),
(34, 'products', '0008_remove_orders_prescriptions_orders_prescription', '2023-11-13 21:08:07.716242'),
(35, 'products', '0007_presciption_order', '2023-11-13 21:46:49.028796'),
(36, 'products', '0008_presciption_order_orders_status_and_more', '2023-11-13 21:46:49.051549'),
(37, 'products', '0009_remove_presciption_order_orders_status', '2023-11-13 21:46:49.063670'),
(38, 'products', '0010_orders_prescriptions', '2023-11-13 21:46:49.084571'),
(41, 'products', '0001_initial', '2023-11-30 06:40:19.381852'),
(42, 'products', '0002_presciption_order_txid_and_more', '2023-11-30 06:40:19.403195');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3hbbzdjqvcm7zprqhdqcl9eizjgdb8m8', '.eJxVj01uAyEMRu_COkIMpEyS7rLvGZCxTYdmBFN-VlHvHkZKpNSSN37Pn-y7cNDb4nrl4iKJi5jE4X3mAW-cdkA_kL6zxJxaiV7uinzSKr8y8Xp9uv8CFqjL2IaJ2B9Jkw_MJ2uUthBssCczg0LUeP5gpuCn6UyzIW8YzVGF2QfUmmY1QrfCFUvcWszJFf7tsfA4rJXOB4EL4y335kZvvYnLXeRSYY2J96c-tVJSjRJ_b27LDdaBtX3BB-vzWvI:1r8s9a:1pwrOLtvz3_CnBC_OGBlB-LQ9gwk925m-CBs3APy99k', '2023-12-22 16:44:44.820660'),
('4ptxphtjg2chjr0r9gu1h4k19zlswowm', '.eJxVjs2uwiAQRt-FtSFQChbvzr3PQAaYWq4NVH5WxneXJproYjZzznzzPYiBVhfTCmYTPDkRSQ7fOwvuhnEH_h_iNVGXYs3B0l2hb1roJXlcz2_3J2CBsvTribtBCTGKIwDz3EvGQKthBA9HPVvB55FpmJQdhZulQKmR-UFJVEI566ceumUsLoethhRNxnsLGXuxGdaCB-IWdLfUqumztUpOD3LpVRFj_87_Bk05Y4w8v8yaKqx7tw97ATfPWL8:1r2rSm:8Cu8qHGy8qBw3wYKRi4c7CNA2NxMaDXCrQR5mF60_ms', '2023-12-06 02:47:42.128098'),
('60snh4vw0ufswkq1djcob4dbhew6q2as', '.eJxVjDkOwjAUBe_iGllegp1Q0ucM0d-MA8iW4qRC3B0ipYD2zcx7qQm2NU9bk2WaWV2UVaffDYEeUnbAdyi3qqmWdZlR74o-aNNjZXleD_fvIEPL3xosC3bsGJNIH7xxAVJIofcRDJGj4SzCCa0dOHpGL-Q7kyImco6jUe8PHo45Rg:1r4IGc:aRW9tQUxmg5xz8YSU40hnK8SbKhQaDM6P9jL7oq7eVE', '2023-12-10 01:37:04.507925'),
('6ells5c7bl9pedy6x8hwaq9p98aza86g', '.eJxVj01uAyEMRu_COkL8TCBJd923V0DGNh2aaJgysIpy9zJSKqULb_yeP9t3EaC3OfSNa8gkLkKLw2svAl552QF9w_JVJJal1Rzlrsgn3eRHIb69P91_ATNs85gGTRwnMhQT88lZZRwkl9zJelCIBs9HZkpR6zN5S9Ey2kklHxMaQ16N0LXyhjWvLZclVP7pufI4rNXOB4Ez47X0FkatvYnLXXzCCmPz9Ka1l04pJR4vXisNbvu__g_-AmHNWTI:1r8awL:ALrSnDUiD8N66zEBJLcgvW-RkFqBJphCknv3Aq4wCeE', '2023-12-21 22:21:55.662096'),
('80brt92uc43tufyufmctkf0qw3hjbph3', '.eJxVjDkOwjAUBe_iGllegp1Q0ucM0d-MA8iW4qRC3B0ipYD2zcx7qQm2NU9bk2WaWV2UVaffDYEeUnbAdyi3qqmWdZlR74o-aNNjZXleD_fvIEPL3xosC3bsGJNIH7xxAVJIofcRDJGj4SzCCa0dOHpGL-Q7kyImco6jUe8PHo45Rg:1rJGGC:SveuQ0-_bBfXj_gVH8q-mX_pVWyrszZyU6Y7dMuIEBo', '2024-01-20 08:30:30.242587'),
('9ngxbuiy4mka8is3mhwj2yburj346juz', '.eJxVjs-OAiEMh9-FsyEMuIy6N-8-AyltcVgnMPLnZPbdFxM30Sa99Pv6ax_CQW-L65WLiyROYhK795kHvHF6AvqBdM0Sc2olevlU5ItWecnE6_nlfgQsUJexDROx35MmH5gP1ihtIdhgD2YGhajx-MVMwU_TkWZD3jCavQqzD6g1zWqEboUrlri1mJMrfO-x8HgswFp5J3BhvOXe3OitN3F6iFwqrDHxOG--rVJSjRK_b27LDdaBrf2Hf0ZsW0c:1rffqF:DrBZAJkyU7S7Ntp_Sgs2MLQKdgzHpJ024GkMhUEiMK4', '2024-03-22 04:16:21.603167'),
('bhf4skfdubi1sujjdy4tr9nikg7i52rx', '.eJxVjLEOgjAURX_FdDZNabEFRnc39-b1vVdBCDVQJuO_WxIGHe5y77nnLTxsuffbyosfSHSiEuffLgCOPO8DPWF-JIlpzssQ5I7IY13lLRFP14P9E_Sw9uUNFXGoSVOIzI01SluINtrGOFCIGtsLM8VQVS05Q8EwmlpFFyJqTU4VKfaMY9qyL3ltuUjvKcPUndQpwwji8wWJOETp:1quBVf:XvjYMNgq5P7nsZpjg47A8MdFIvUiU6Y3c4FXjVdoRcc', '2023-11-12 04:22:49.403059'),
('nf1wny7z631fllzqjno1dj0ijwkn39s8', '.eJxVjz1uAyEQhe9CbSEWNrBrd-mdK6CBGbLEFmxYqKzcPRC5cIppvvejNw9modXNtoOKjcjObGKnV-bA3ygNAb8gfWbuc6olOj4s_Kke_JqR7u9P77-CDY6tp2FCcjNKdIFo0UpIDUEHvSgDwnvp1zciDG6aVjQKnSKvZhGMC15KNKKX7oUOX-JeY0620HeLhfqwWhqdmN_I33Krtt_eKjs_2AfsMB66yJXPQoyKax9PlDpVl8VwNejPS7jmCveRMZqbP_EX069ekQ:1r8qS5:RFdmlZCzswmd_VYRu31MTn3WI9Nhekg6gSZ5PRat_C4', '2023-12-22 14:55:43.187552'),
('qoh5f63w39x3qe6gof05v8ajz46d5qma', '.eJxVjDkOwjAUBe_iGllegp1Q0ucM0d-MA8iW4qRC3B0ipYD2zcx7qQm2NU9bk2WaWV2UVaffDYEeUnbAdyi3qqmWdZlR74o-aNNjZXleD_fvIEPL3xosC3bsGJNIH7xxAVJIofcRDJGj4SzCCa0dOHpGL-Q7kyImco6jUe8PHo45Rg:1qsVfu:YsWSmVQSXrI08L-nrLcAaFILdz2ZY7_bv3RsmyY4qNs', '2023-11-07 13:30:28.872023'),
('qvyo84cvz6g4i7i3c7m7nlrf7qb430mx', '.eJxVjDkOwjAUBe_iGllegp1Q0ucM0d-MA8iW4qRC3B0ipYD2zcx7qQm2NU9bk2WaWV2UVaffDYEeUnbAdyi3qqmWdZlR74o-aNNjZXleD_fvIEPL3xosC3bsGJNIH7xxAVJIofcRDJGj4SzCCa0dOHpGL-Q7kyImco6jUe8PHo45Rg:1r4Hi3:4Da8x2bwPr0r_ZHT9X_ewOzGjvIro9Ssb51CHYc-5zU', '2023-12-10 01:01:21.131149'),
('se8gj4zsewd8mph5qy33f7aceyiewjrj', '.eJxVjDkOwjAUBe_iGllegp1Q0ucM0d-MA8iW4qRC3B0ipYD2zcx7qQm2NU9bk2WaWV2UVaffDYEeUnbAdyi3qqmWdZlR74o-aNNjZXleD_fvIEPL3xosC3bsGJNIH7xxAVJIofcRDJGj4SzCCa0dOHpGL-Q7kyImco6jUe8PHo45Rg:1rJBuz:oNj-L8rQL8KSXj0L8rpLG1PevUc0Bclaxw83bme0TD4', '2024-01-20 03:52:19.610490');

-- --------------------------------------------------------

--
-- Table structure for table `home_product`
--

CREATE TABLE `home_product` (
  `p_name` varchar(25) NOT NULL,
  `p_category` varchar(25) NOT NULL,
  `p_price` decimal(10,2) NOT NULL,
  `p_discount` decimal(5,2) NOT NULL,
  `p_id` int(20) NOT NULL,
  `p_image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `home_product`
--

INSERT INTO `home_product` (`p_name`, `p_category`, `p_price`, `p_discount`, `p_id`, `p_image`) VALUES
('Napa', 'BABY CARE', 30.00, 2.00, 1, 'media/napaextra_GVuCZeT.jpg'),
('Monteen', 'Neurological Problems', 30.00, 3.00, 2, 'media/napasyrup_zzE29SU.jpg'),
('orsaline', 'Heart Problems', 200.00, 0.00, 3, 'media/b.png');

-- --------------------------------------------------------

--
-- Table structure for table `products_main_product`
--

CREATE TABLE `products_main_product` (
  `p_id` int(11) NOT NULL,
  `p_name` varchar(255) NOT NULL,
  `p_type` varchar(255) NOT NULL,
  `p_image` varchar(100) NOT NULL,
  `p_generics` varchar(255) NOT NULL,
  `p_company` varchar(255) NOT NULL,
  `medPerStrip` decimal(10,2) NOT NULL,
  `p_price` decimal(10,2) NOT NULL,
  `p_discount` decimal(5,2) NOT NULL,
  `p_Indications` longtext NOT NULL,
  `p_Pharmacology` longtext NOT NULL,
  `p_Dosage` longtext NOT NULL,
  `p_Interaction` longtext NOT NULL,
  `p_Contradictions` longtext NOT NULL,
  `p_Side_Effects` longtext NOT NULL,
  `p_Pregnancy` longtext NOT NULL,
  `p_Precautions` longtext NOT NULL,
  `p_Therapeutic` longtext NOT NULL,
  `p_Storage` varchar(255) NOT NULL,
  `p_category` varchar(255) NOT NULL,
  `feature` varchar(255) NOT NULL,
  `otc_status` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `products_main_product`
--

INSERT INTO `products_main_product` (`p_id`, `p_name`, `p_type`, `p_image`, `p_generics`, `p_company`, `medPerStrip`, `p_price`, `p_discount`, `p_Indications`, `p_Pharmacology`, `p_Dosage`, `p_Interaction`, `p_Contradictions`, `p_Side_Effects`, `p_Pregnancy`, `p_Precautions`, `p_Therapeutic`, `p_Storage`, `p_category`, `feature`, `otc_status`) VALUES
(1, 'Napa', 'Medicine', 'media/napaextra_GVuCZeT.jpg', 'ccjbcjsbcdsdsd', 'sdsdsd', 10.00, 30.00, 2.00, 'gctfgbukbbubkjb', 'dxgfchgvjhbkjnluyftdrdsertryctvuybhkjn', 'rdtvybunimiuytfrdes', 'zexrctvybunimojiu7g65', 'extcfvghjhbkjnlbhvgcfxt', 'xcfgvhbjnkmiuygtf', 'vfxtrfcgvjhbkjnlubigyuft', 'ccfvygbuhnijnbhugvyfctc', 'cfvgbhnjjhbuvgy', 'huiyiuh', 'BABY CARE', 'yes', 'no'),
(2, 'Monteen', 'Medicine', 'media/napasyrup_zzE29SU.jpg', 'bbduasbduia', 'dsdsd', 10.00, 30.00, 3.00, 'rvytbuyniunyubtyvrcexectfvygbuhni', 'xctvygbuhnijvctxrctfvygbuh', 'xdcfvgbhnbugvyftcrxctvygbuhn', 'xrdctfvygbuhnijbuyvrtcerxrectfvygbuhn', 'dxrctfvgybhunjhbuyvtcrexctfvygbuhn', 'rxdctfvgybhnbgvyfctdrxdctfvygbh', 'dxdctfvgbhjnkbhugvyfctfxrdctfvygb', 'drctfvygbhnbgvfctxrdctfvygb', 'sxdcfvgbhnjhbgyvftcrctfvygbh', 'Cold', 'Neurological Problems', 'yes', 'yes'),
(3, 'orsaline', 'pet kharap', 'media/b.png', 'yg', 'gg', 24.00, 200.00, 0.00, 'fggf', 'ghfhfh', 'fhfhf', 'fhf', 'hfhfh', 'fhfh', 'fhfh', 'fhfh', 'fhfhfh', 'fhfhfh', 'Heart Problems', 'yes', 'yes');

-- --------------------------------------------------------

--
-- Table structure for table `products_orders`
--

CREATE TABLE `products_orders` (
  `id` int(11) NOT NULL,
  `phonenumber` text NOT NULL,
  `ordered_products` text NOT NULL,
  `total` text NOT NULL,
  `del_adress` text NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `prescriptions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`prescriptions`)),
  `Delivery_status` varchar(20) NOT NULL,
  `TxID` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `paymentMobile` varchar(15) CHARACTER SET latin1 COLLATE latin1_spanish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products_orders`
--

INSERT INTO `products_orders` (`id`, `phonenumber`, `ordered_products`, `total`, `del_adress`, `timestamp`, `status`, `prescriptions`, `Delivery_status`, `TxID`, `paymentMobile`) VALUES
(47, '+88001955112789', '[(\'Napa\', \'4\', \'117.6000\')]', '177.6000', 'Wst Masird', '2023-11-30 06:56:15.992207', 'pending', '[\"otc_prescription/+88001955112789/_7807867.jpg\"]', 'Pending', NULL, NULL),
(48, '+88001955112789', '[(\'Napa\', \'4\', \'117.6000\')]', '177.6000', 'savdhssav', '2023-11-30 07:00:40.066624', 'pending', '[\"otc_prescription/+88001955112789/_7807867_l5ENjAr.jpg\"]', 'Pending', 'ybsbaidsnan', '01955112789');

-- --------------------------------------------------------

--
-- Table structure for table `products_presciption_order`
--

CREATE TABLE `products_presciption_order` (
  `id` bigint(20) NOT NULL,
  `phonenumber` varchar(15) NOT NULL,
  `prescription_img` longtext NOT NULL,
  `days` longtext NOT NULL,
  `del_adress` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `Delivery_status` varchar(20) NOT NULL,
  `TxID` varchar(50) DEFAULT NULL,
  `paymentMobile` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `products_presciption_order`
--

INSERT INTO `products_presciption_order` (`id`, `phonenumber`, `prescription_img`, `days`, `del_adress`, `timestamp`, `status`, `Delivery_status`, `TxID`, `paymentMobile`) VALUES
(11, '+88001955112789', 'prescription/+88001955112789/1700575448432.png', '15', '8dbai', '2023-11-30 23:00:59.646998', 'Pending', 'Pending', 'A wxwwc', '2f2f');

-- --------------------------------------------------------

--
-- Table structure for table `products_profile_medlist`
--

CREATE TABLE `products_profile_medlist` (
  `phone_number` varchar(15) NOT NULL,
  `med_list` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`med_list`)),
  `prescriptions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`prescriptions`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products_profile_medlist`
--

INSERT INTO `products_profile_medlist` (`phone_number`, `med_list`, `prescriptions`) VALUES
('+88001955112789', '{\"2\": [[\"Morning\"], 1], \"1\": [[\"Night\"], 1]}', '[[\"prescription/+88001955112789/Nutri + Logo+N (1) (2).png\", \"15\"], [\"prescription/+88001955112789/Medal_mockup_04.jpg\", \"15\"], [\"prescription/+88001955112789/Medal_mockup_04_Gaz25mP.jpg\", \"15\"], [\"prescription/+88001955112789/1700575448432.png\", \"15\"]]');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authentication_userprofile`
--
ALTER TABLE `authentication_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- Indexes for table `authentication_userprofile_groups`
--
ALTER TABLE `authentication_userprofile_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `authentication_userprofi_userprofile_id_group_id_888adc9b_uniq` (`userprofile_id`,`group_id`),
  ADD KEY `authentication_userp_group_id_b929d111_fk_auth_grou` (`group_id`);

--
-- Indexes for table `authentication_userprofile_user_permissions`
--
ALTER TABLE `authentication_userprofile_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `authentication_userprofi_userprofile_id_permissio_8399fac0_uniq` (`userprofile_id`,`permission_id`),
  ADD KEY `authentication_userp_permission_id_b416f4d8_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_authentic` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `home_product`
--
ALTER TABLE `home_product`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `products_main_product`
--
ALTER TABLE `products_main_product`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `products_orders`
--
ALTER TABLE `products_orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products_presciption_order`
--
ALTER TABLE `products_presciption_order`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products_profile_medlist`
--
ALTER TABLE `products_profile_medlist`
  ADD PRIMARY KEY (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `authentication_userprofile`
--
ALTER TABLE `authentication_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `authentication_userprofile_groups`
--
ALTER TABLE `authentication_userprofile_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `authentication_userprofile_user_permissions`
--
ALTER TABLE `authentication_userprofile_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `home_product`
--
ALTER TABLE `home_product`
  MODIFY `p_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products_main_product`
--
ALTER TABLE `products_main_product`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products_orders`
--
ALTER TABLE `products_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `products_presciption_order`
--
ALTER TABLE `products_presciption_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authentication_userprofile_groups`
--
ALTER TABLE `authentication_userprofile_groups`
  ADD CONSTRAINT `authentication_userp_group_id_b929d111_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `authentication_userp_userprofile_id_01c22330_fk_authentic` FOREIGN KEY (`userprofile_id`) REFERENCES `authentication_userprofile` (`id`);

--
-- Constraints for table `authentication_userprofile_user_permissions`
--
ALTER TABLE `authentication_userprofile_user_permissions`
  ADD CONSTRAINT `authentication_userp_permission_id_b416f4d8_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `authentication_userp_userprofile_id_0ed47435_fk_authentic` FOREIGN KEY (`userprofile_id`) REFERENCES `authentication_userprofile` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_userprofile` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
