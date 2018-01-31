-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2018-01-31 12:06:48
-- 服务器版本： 5.7.11
-- PHP Version: 5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `creditchina`
--

-- --------------------------------------------------------

--
-- 表的结构 `cust_attention_list`
--

CREATE TABLE `cust_attention_list` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(256) DEFAULT NULL,
  `data_source` varchar(80) DEFAULT NULL,
  `comp_name` varchar(256) DEFAULT NULL,
  `reg_no` varchar(80) DEFAULT NULL,
  `legal_person` varchar(80) DEFAULT NULL,
  `exception_reason_type` varchar(1024) DEFAULT NULL,
  `set_date` varchar(10) DEFAULT NULL,
  `org_name` varchar(256) DEFAULT NULL,
  `data_update_date` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `cust_red_list`
--

CREATE TABLE `cust_red_list` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(256) DEFAULT NULL,
  `data_source` varchar(80) DEFAULT NULL,
  `no` varchar(80) DEFAULT NULL,
  `taxpayer_name` varchar(256) DEFAULT NULL,
  `rating_year` varchar(10) DEFAULT NULL,
  `data_update_date` varchar(32) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dishonesty_blacklist`
--

CREATE TABLE `dishonesty_blacklist` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(256) DEFAULT NULL,
  `data_source` varchar(80) DEFAULT NULL,
  `case_no` varchar(256) DEFAULT NULL,
  `dishonesty_cust_name` varchar(256) DEFAULT NULL,
  `legal_person` varchar(80) DEFAULT NULL,
  `exec_court` varchar(256) DEFAULT NULL,
  `area_name` varchar(256) DEFAULT NULL,
  `exec_gist_no` varchar(256) DEFAULT NULL,
  `exec_gist_org` varchar(256) DEFAULT NULL,
  `writ_content` text,
  `performance_status` varchar(1024) DEFAULT NULL,
  `dishonesty_cust_specific_status` varchar(1024) DEFAULT NULL,
  `issue_date` varchar(10) DEFAULT NULL,
  `register_date` varchar(10) DEFAULT NULL,
  `performanced_part` varchar(1024) DEFAULT NULL,
  `unperformanced_part` varchar(10) DEFAULT NULL,
  `data_update_date` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `pub_permissions_name`
--

CREATE TABLE `pub_permissions_name` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(255) DEFAULT NULL,
  `adm_license_writ_no` varchar(80) DEFAULT NULL,
  `audit_type` varchar(80) DEFAULT NULL,
  `legal_person` varchar(256) DEFAULT NULL,
  `content` varchar(1024) DEFAULT NULL,
  `permit_validity` varchar(10) DEFAULT NULL,
  `permit_decision_date` varchar(10) DEFAULT NULL,
  `permit_issue_date` varchar(10) DEFAULT NULL,
  `local_code` varchar(80) DEFAULT NULL,
  `permit_org` varchar(256) DEFAULT NULL,
  `data_update_date` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `purchasing_badness_record`
--

CREATE TABLE `purchasing_badness_record` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(256) DEFAULT NULL,
  `data_source` varchar(80) DEFAULT NULL,
  `supplier_name` varchar(256) DEFAULT NULL,
  `supplier_addr` varchar(1024) DEFAULT NULL,
  `lawless_status` varchar(1024) DEFAULT NULL,
  `punish_result` varchar(1024) DEFAULT NULL,
  `punish_gist` varchar(1024) DEFAULT NULL,
  `punish_date` varchar(10) DEFAULT NULL,
  `exec_org` varchar(256) DEFAULT NULL,
  `punish_end_date` varchar(10) DEFAULT NULL,
  `data_update_date` varchar(32) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `serious_revenue_lawless_cust_list`
--

CREATE TABLE `serious_revenue_lawless_cust_list` (
  `batch_date` varchar(10) DEFAULT NULL,
  `cust_name` varchar(256) DEFAULT NULL,
  `data_source` varchar(80) DEFAULT NULL,
  `taxer_name` varchar(256) DEFAULT NULL,
  `taxer_id` varchar(80) DEFAULT NULL,
  `org_code` varchar(80) DEFAULT NULL,
  `register_addr` varchar(256) DEFAULT NULL,
  `legal_person_name` varchar(80) DEFAULT NULL,
  `financing_person_name` varchar(80) DEFAULT NULL,
  `intermediary_info` varchar(1024) DEFAULT NULL,
  `case_nature` varchar(1024) DEFAULT NULL,
  `lawless_fact` text,
  `punish_status` text,
  `case_report_date` varchar(80) DEFAULT NULL,
  `data_update_date` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
