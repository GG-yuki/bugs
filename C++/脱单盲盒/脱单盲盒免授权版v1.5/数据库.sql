-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2021-09-27 11:13:17
-- 服务器版本： 5.6.47-log
-- PHP Version: 7.3.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mhcs_yizhanhongt`
--

-- --------------------------------------------------------

--
-- 表的结构 `asset`
--

CREATE TABLE `asset` (
  `id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `filename` varchar(128) NOT NULL,
  `savename` varchar(255) NOT NULL,
  `filesize` int(11) NOT NULL,
  `ext` varchar(8) NOT NULL,
  `create_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '组名',
  `rules` text COMMENT '规则ID',
  `remark` varchar(255) DEFAULT NULL,
  `create_time` int(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间',
  `status` varchar(30) NOT NULL DEFAULT '' COMMENT '状态'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分组表' ROW_FORMAT=COMPACT;

--
-- 转存表中的数据 `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`, `rules`, `remark`, `create_time`, `update_time`, `status`) VALUES
(1, '管理员', '824,826,827,828,829,830,831,832,833,834,825,835,836,837,838,839,840,841,842,843,868,869,870,871,872,873,874,875,876,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,55,315,316,317,318,319,320,321,322,138,139,140,141,142,143,144,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,57,375,376,377,702,703,704,705,706,707,708,709,510,512,513,514,515,516,517,511,1,2,3,4,5,6,7,8,9,867,10,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,121,122,123,124,125,126,127,128,440,441,442,443,444,445,446,447,351,352,353,354,355,356,357,358,11,12,13,14,15,16,17,18,19,20,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858', '', 0, 1631529566, '1'),
(2, '临时组', '', '', 1631605609, 1631605609, '1');

-- --------------------------------------------------------

--
-- 表的结构 `auth_group_access`
--

CREATE TABLE `auth_group_access` (
  `uid` int(10) UNSIGNED NOT NULL COMMENT '会员ID',
  `group_id` int(10) UNSIGNED NOT NULL COMMENT '级别ID'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限分组表' ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- 表的结构 `auth_rule`
--

CREATE TABLE `auth_rule` (
  `id` int(10) UNSIGNED NOT NULL,
  `title` varchar(50) NOT NULL DEFAULT '' COMMENT '规则名称',
  `pid` int(11) NOT NULL,
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '规则唯一标识',
  `condition` varchar(255) NOT NULL DEFAULT '' COMMENT '条件',
  `icon` varchar(50) NOT NULL DEFAULT '' COMMENT '图标',
  `remark` varchar(255) NOT NULL DEFAULT '' COMMENT '备注',
  `is_menu` tinyint(1) UNSIGNED NOT NULL DEFAULT '0' COMMENT '是否为菜单',
  `create_time` int(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(11) UNSIGNED NOT NULL DEFAULT '0' COMMENT '更新时间',
  `sort` int(10) NOT NULL DEFAULT '0' COMMENT '权重',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='节点表' ROW_FORMAT=COMPACT;

--
-- 转存表中的数据 `auth_rule`
--

INSERT INTO `auth_rule` (`id`, `title`, `pid`, `name`, `condition`, `icon`, `remark`, `is_menu`, `create_time`, `update_time`, `sort`, `status`) VALUES
(1, '网站设置', 0, 'SettingFolder', '', 'fa fa-sitemap', '', 1, 1538816580, 1576723164, 20, 1),
(2, '网站配置', 1, 'Siteinfo/index', '', '', '', 1, 0, 1538816676, 0, 1),
(3, '添加', 2, 'Siteinfo/add', '', '', '', 0, 0, 0, 0, 1),
(4, '提交添加', 2, 'Siteinfo/add_post', '', '', '', 0, 0, 0, 0, 1),
(5, '编辑', 2, 'Siteinfo/edit', '', '', '', 0, 0, 0, 0, 1),
(6, '提交编辑', 2, 'Siteinfo/edit_post', '', '', '', 0, 0, 0, 0, 1),
(7, '删除', 2, 'Siteinfo/delete', '', '', '', 0, 0, 0, 0, 1),
(8, '排序', 2, 'Siteinfo/setsort', '', '', '', 0, 0, 0, 0, 1),
(9, '设置状态', 2, 'Siteinfo/setstatus', '', '', '', 0, 0, 0, 0, 1),
(10, '系统设置', 0, 'SystemFolder', '', 'fa fa-cog', '', 1, 1538816700, 1576723229, 10, 1),
(11, '后台菜单', 10, 'AuthRule/index', '', '', '', 1, 0, 0, 1, 1),
(12, '添加', 11, 'AuthRule/add', '', '', '', 0, 0, 0, 0, 1),
(13, '提交添加', 11, 'AuthRule/add_post', '', '', '', 0, 0, 0, 0, 1),
(14, '编辑', 11, 'AuthRule/edit', '', '', '', 0, 0, 0, 0, 1),
(15, '提交编辑', 11, 'AuthRule/edit_post', '', '', '', 0, 0, 0, 0, 1),
(16, '删除', 11, 'AuthRule/delete', '', '', '', 0, 0, 0, 0, 1),
(17, '排序', 11, 'AuthRule/setsort', '', '', '', 0, 0, 0, 0, 1),
(18, '设置状态', 11, 'AuthRule/setstatus', '', '', '', 0, 0, 0, 0, 1),
(19, '未知', 11, 'AuthRule/addc', '', '', '', 0, 0, 0, 0, 1),
(20, '未知', 11, 'AuthRule/addc_post', '', '', '', 0, 0, 0, 0, 1),
(21, '管理员', 10, 'User/index', '', '', '', 1, 0, 0, 9, 1),
(22, '添加', 21, 'User/add', '', '', '', 0, 0, 0, 0, 1),
(23, '提交添加', 21, 'User/add_post', '', '', '', 0, 0, 0, 0, 1),
(24, '编辑', 21, 'User/edit', '', '', '', 0, 0, 0, 0, 1),
(25, '提交编辑', 21, 'User/edit_post', '', '', '', 0, 0, 0, 0, 1),
(26, '删除', 21, 'User/delete', '', '', '', 0, 0, 0, 0, 1),
(27, '排序', 21, 'User/setsort', '', '', '', 0, 0, 0, 0, 1),
(28, '设置状态', 21, 'User/setstatus', '', '', '', 0, 0, 0, 0, 1),
(29, '未知', 21, 'User/pwd', '', '', '', 0, 0, 0, 0, 1),
(30, '未知', 21, 'User/pwd_post', '', '', '', 0, 0, 0, 0, 1),
(31, '用户组', 10, 'AuthGroup/index', '', '', '', 1, 0, 0, 8, 1),
(32, '添加', 31, 'AuthGroup/add', '', '', '', 0, 0, 0, 0, 1),
(33, '提交添加', 31, 'AuthGroup/add_post', '', '', '', 0, 0, 0, 0, 1),
(34, '编辑', 31, 'AuthGroup/edit', '', '', '', 0, 0, 0, 0, 1),
(35, '提交编辑', 31, 'AuthGroup/edit_post', '', '', '', 0, 0, 0, 0, 1),
(36, '删除', 31, 'AuthGroup/delete', '', '', '', 0, 0, 0, 0, 1),
(37, '排序', 31, 'AuthGroup/setsort', '', '', '', 0, 0, 0, 0, 1),
(38, '设置状态', 31, 'AuthGroup/setstatus', '', '', '', 0, 0, 0, 0, 1),
(55, '营销推广', 0, 'PromoteFolder', '', 'fa fa-bullhorn', '', 1, 1540376695, 1576723253, 50, 1),
(57, '日志', 0, 'LogFolder', '', 'fa fa-edit', '', 1, 1540376734, 1576723075, 40, 1),
(103, '广告', 55, 'BannerWrap', '', '', '', 1, 1540525074, 1540525074, 0, 1),
(104, '广告位', 103, 'BannerPosition/index', '', '', '', 1, 0, 0, 0, 1),
(105, '添加', 104, 'BannerPosition/add', '', '', '', 0, 0, 0, 0, 1),
(106, '提交添加', 104, 'BannerPosition/add_post', '', '', '', 0, 0, 0, 0, 1),
(107, '编辑', 104, 'BannerPosition/edit', '', '', '', 0, 0, 0, 0, 1),
(108, '提交编辑', 104, 'BannerPosition/edit_post', '', '', '', 0, 0, 0, 0, 1),
(109, '删除', 104, 'BannerPosition/delete', '', '', '', 0, 0, 0, 0, 1),
(110, '排序', 104, 'BannerPosition/setsort', '', '', '', 0, 0, 0, 0, 1),
(111, '设置状态', 104, 'BannerPosition/setstatus', '', '', '', 0, 0, 0, 0, 1),
(112, '广告管理', 103, 'Banner/index', '', '', '', 1, 0, 0, 0, 1),
(113, '添加', 112, 'Banner/add', '', '', '', 0, 0, 0, 0, 1),
(114, '提交添加', 112, 'Banner/add_post', '', '', '', 0, 0, 0, 0, 1),
(115, '编辑', 112, 'Banner/edit', '', '', '', 0, 0, 0, 0, 1),
(116, '提交编辑', 112, 'Banner/edit_post', '', '', '', 0, 0, 0, 0, 1),
(117, '删除', 112, 'Banner/delete', '', '', '', 0, 0, 0, 0, 1),
(118, '排序', 112, 'Banner/setsort', '', '', '', 0, 0, 0, 0, 1),
(119, '设置状态', 112, 'Banner/setstatus', '', '', '', 0, 0, 0, 0, 1),
(120, '上传文件', 112, 'Banner/uploadfile', '', '', '', 0, 0, 0, 0, 1),
(121, '语言管理', 10, 'Lang/index', '', '', '', 0, 0, 0, 6, 1),
(122, '添加', 121, 'Lang/add', '', '', '', 0, 0, 0, 0, 1),
(123, '提交添加', 121, 'Lang/add_post', '', '', '', 0, 0, 0, 0, 1),
(124, '编辑', 121, 'Lang/edit', '', '', '', 0, 0, 0, 0, 1),
(125, '提交编辑', 121, 'Lang/edit_post', '', '', '', 0, 0, 0, 0, 1),
(126, '删除', 121, 'Lang/delete', '', '', '', 0, 0, 0, 0, 1),
(127, '排序', 121, 'Lang/setsort', '', '', '', 0, 0, 0, 0, 1),
(128, '设置状态', 121, 'Lang/setstatus', '', '', '', 0, 0, 0, 0, 1),
(138, '推广链接', 315, 'Links/index', '', '', '', 1, 0, 1542852982, 0, 1),
(139, '添加', 138, 'Links/add', '', '', '', 0, 0, 0, 0, 1),
(140, '提交添加', 138, 'Links/add_post', '', '', '', 0, 0, 0, 0, 1),
(141, '编辑', 138, 'Links/edit', '', '', '', 0, 0, 0, 0, 1),
(142, '提交编辑', 138, 'Links/edit_post', '', '', '', 0, 0, 0, 0, 1),
(143, '删除', 138, 'Links/delete', '', '', '', 0, 0, 0, 0, 1),
(144, '设置状态', 138, 'Links/setstatus', '', '', '', 0, 0, 0, 0, 1),
(315, '推广链接', 55, '', '', '', '', 1, 1542852965, 1542852965, 0, 1),
(316, '推广分类', 315, 'LinksCategory/index', '', '', '', 1, 0, 0, 0, 1),
(317, '添加', 316, 'LinksCategory/add', '', '', '', 0, 0, 0, 0, 1),
(318, '提交添加', 316, 'LinksCategory/add_post', '', '', '', 0, 0, 0, 0, 1),
(319, '编辑', 316, 'LinksCategory/edit', '', '', '', 0, 0, 0, 0, 1),
(320, '提交编辑', 316, 'LinksCategory/edit_post', '', '', '', 0, 0, 0, 0, 1),
(321, '删除', 316, 'LinksCategory/delete', '', '', '', 0, 0, 0, 0, 1),
(322, '排序', 316, 'LinksCategory/setsort', '', '', '', 0, 0, 0, 0, 1),
(351, '信息模板', 10, 'MsgTemplate/index', '', '', '', 0, 0, 1622189395, 4, 1),
(352, '添加', 351, 'MsgTemplate/add', '', '', '', 0, 0, 0, 0, 1),
(353, '提交添加', 351, 'MsgTemplate/add_post', '', '', '', 0, 0, 0, 0, 1),
(354, '编辑', 351, 'MsgTemplate/edit', '', '', '', 0, 0, 0, 0, 1),
(355, '提交编辑', 351, 'MsgTemplate/edit_post', '', '', '', 0, 0, 0, 0, 1),
(356, '删除', 351, 'MsgTemplate/delete', '', '', '', 0, 0, 0, 0, 1),
(357, '排序', 351, 'MsgTemplate/setsort', '', '', '', 0, 0, 0, 0, 1),
(358, '设置状态', 351, 'MsgTemplate/setstatus', '', '', '', 0, 0, 0, 0, 1),
(375, '邮件发送日志', 57, 'EmailLog/index', '', '', '', 0, 0, 0, 0, 1),
(376, '删除', 375, 'EmailLog/delete', '', '', '', 0, 0, 0, 0, 1),
(377, '查看', 375, 'EmailLog/edit', '', '', '', 0, 0, 0, 0, 1),
(440, '内容模板', 10, 'ContentTemplate/index', '', '', '', 0, 0, 0, 5, 1),
(441, '添加', 440, 'ContentTemplate/add', '', '', '', 0, 0, 0, 0, 1),
(442, '提交添加', 440, 'ContentTemplate/add_post', '', '', '', 0, 0, 0, 0, 1),
(443, '编辑', 440, 'ContentTemplate/edit', '', '', '', 0, 0, 0, 0, 1),
(444, '提交编辑', 440, 'ContentTemplate/edit_post', '', '', '', 0, 0, 0, 0, 1),
(445, '删除', 440, 'ContentTemplate/delete', '', '', '', 0, 0, 0, 0, 1),
(446, '排序', 440, 'ContentTemplate/setsort', '', '', '', 0, 0, 0, 0, 1),
(447, '设置状态', 440, 'ContentTemplate/setstatus', '', '', '', 0, 0, 0, 0, 1),
(510, '短信日志', 57, 'SmsLog/index', '', '', '', 0, 0, 0, 0, 1),
(511, '添加', 510, 'SmsLog/add', '', '', '', 0, 0, 0, 0, 1),
(512, '提交添加', 510, 'SmsLog/add_post', '', '', '', 0, 0, 0, 0, 1),
(513, '编辑', 510, 'SmsLog/edit', '', '', '', 0, 0, 0, 0, 1),
(514, '提交编辑', 510, 'SmsLog/edit_post', '', '', '', 0, 0, 0, 0, 1),
(515, '删除', 510, 'SmsLog/delete', '', '', '', 0, 0, 0, 0, 1),
(516, '排序', 510, 'SmsLog/setsort', '', '', '', 0, 0, 0, 0, 1),
(517, '设置状态', 510, 'SmsLog/setstatus', '', '', '', 0, 0, 0, 0, 1),
(635, '新闻管理', 0, 'NewsWrap', '', 'fa fa-newspaper-o', '', 1, 1622172874, 1622172874, 90, 1),
(636, '新闻列表', 635, 'News/index', '', '', '', 1, 0, 0, 0, 1),
(637, '添加', 636, 'News/add', '', '', '', 0, 0, 0, 0, 1),
(638, '提交添加', 636, 'News/add_post', '', '', '', 0, 0, 0, 0, 1),
(639, '编辑', 636, 'News/edit', '', '', '', 0, 0, 0, 0, 1),
(640, '提交编辑', 636, 'News/edit_post', '', '', '', 0, 0, 0, 0, 1),
(641, '删除', 636, 'News/delete', '', '', '', 0, 0, 0, 0, 1),
(642, '排序', 636, 'News/setsort', '', '', '', 0, 0, 0, 0, 1),
(643, '设置状态', 636, 'News/setstatus', '', '', '', 0, 0, 0, 0, 1),
(644, '上传文件', 636, 'News/uploadfile', '', '', '', 0, 0, 0, 0, 1),
(645, '新闻分类', 635, 'NewsCategory/index', '', '', '', 1, 0, 0, 0, 1),
(646, '添加', 645, 'NewsCategory/add', '', '', '', 0, 0, 0, 0, 1),
(647, '提交添加', 645, 'NewsCategory/add_post', '', '', '', 0, 0, 0, 0, 1),
(648, '编辑', 645, 'NewsCategory/edit', '', '', '', 0, 0, 0, 0, 1),
(649, '提交编辑', 645, 'NewsCategory/edit_post', '', '', '', 0, 0, 0, 0, 1),
(650, '删除', 645, 'NewsCategory/delete', '', '', '', 0, 0, 0, 0, 1),
(651, '排序', 645, 'NewsCategory/setsort', '', '', '', 0, 0, 0, 0, 1),
(652, '设置状态', 645, 'NewsCategory/setstatus', '', '', '', 0, 0, 0, 0, 1),
(653, '上传文件', 645, 'NewsCategory/uploadfile', '', '', '', 0, 0, 0, 0, 1),
(673, '合作伙伴', 0, 'PartnerWrap', '', 'fa fa-handshake-o', '', 1, 1622173040, 1622173040, 70, 1),
(674, '合作列表', 673, 'Partner/index', '', '', '', 1, 0, 0, 0, 1),
(675, '添加', 674, 'Partner/add', '', '', '', 0, 0, 0, 0, 1),
(676, '提交添加', 674, 'Partner/add_post', '', '', '', 0, 0, 0, 0, 1),
(677, '编辑', 674, 'Partner/edit', '', '', '', 0, 0, 0, 0, 1),
(678, '提交编辑', 674, 'Partner/edit_post', '', '', '', 0, 0, 0, 0, 1),
(679, '删除', 674, 'Partner/delete', '', '', '', 0, 0, 0, 0, 1),
(680, '排序', 674, 'Partner/setsort', '', '', '', 0, 0, 0, 0, 1),
(681, '设置状态', 674, 'Partner/setstatus', '', '', '', 0, 0, 0, 0, 1),
(682, '上传文件', 674, 'Partner/uploadfile', '', '', '', 0, 0, 0, 0, 1),
(683, '未知', 674, 'Partner/uploadimage', '', '', '', 0, 0, 0, 0, 1),
(684, '合作伙伴分类', 673, 'PartnerCategory/index', '', '', '', 1, 0, 0, 0, 1),
(685, '添加', 684, 'PartnerCategory/add', '', '', '', 0, 0, 0, 0, 1),
(686, '提交添加', 684, 'PartnerCategory/add_post', '', '', '', 0, 0, 0, 0, 1),
(687, '编辑', 684, 'PartnerCategory/edit', '', '', '', 0, 0, 0, 0, 1),
(688, '提交编辑', 684, 'PartnerCategory/edit_post', '', '', '', 0, 0, 0, 0, 1),
(689, '删除', 684, 'PartnerCategory/delete', '', '', '', 0, 0, 0, 0, 1),
(690, '排序', 684, 'PartnerCategory/setsort', '', '', '', 0, 0, 0, 0, 1),
(691, '设置状态', 684, 'PartnerCategory/setstatus', '', '', '', 0, 0, 0, 0, 1),
(702, '管理员操作日志', 57, 'UserLog/index', '', '', '', 1, 0, 0, 0, 1),
(703, '添加', 702, 'UserLog/add', '', '', '', 0, 0, 0, 0, 1),
(704, '提交添加', 702, 'UserLog/add_post', '', '', '', 0, 0, 0, 0, 1),
(705, '编辑', 702, 'UserLog/edit', '', '', '', 0, 0, 0, 0, 1),
(706, '提交编辑', 702, 'UserLog/edit_post', '', '', '', 0, 0, 0, 0, 1),
(707, '删除', 702, 'UserLog/delete', '', '', '', 0, 0, 0, 0, 1),
(708, '排序', 702, 'UserLog/setsort', '', '', '', 0, 0, 0, 0, 1),
(709, '设置状态', 702, 'UserLog/setstatus', '', '', '', 0, 0, 0, 0, 1),
(824, '留一个', 0, 'Stay', '', 'fa fa-send-o', '', 1, 1630738764, 1630738764, 500, 1),
(825, '取一个', 0, 'Take', '', 'fa fa-hand-lizard-o', '', 1, 1630738765, 1630738765, 400, 1),
(826, '数据列表', 824, 'Stay/index', '', '', '', 1, 0, 0, 0, 1),
(827, '添加', 826, 'Stay/add', '', '', '', 0, 0, 0, 0, 1),
(828, '提交添加', 826, 'Stay/add_post', '', '', '', 0, 0, 0, 0, 1),
(829, '编辑', 826, 'Stay/edit', '', '', '', 0, 0, 0, 0, 1),
(830, '提交编辑', 826, 'Stay/edit_post', '', '', '', 0, 0, 0, 0, 1),
(831, '删除', 826, 'Stay/delete', '', '', '', 0, 0, 0, 0, 1),
(832, '排序', 826, 'Stay/setsort', '', '', '', 0, 0, 0, 0, 1),
(833, '设置状态', 826, 'Stay/setstatus', '', '', '', 0, 0, 0, 0, 1),
(834, '导出数据', 826, 'Stay/export', '', '', '', 0, 0, 0, 0, 1),
(835, '数据列表', 825, 'Take/index', '', '', '', 1, 0, 0, 0, 1),
(836, '添加', 835, 'Take/add', '', '', '', 0, 0, 0, 0, 1),
(837, '提交添加', 835, 'Take/add_post', '', '', '', 0, 0, 0, 0, 1),
(838, '编辑', 835, 'Take/edit', '', '', '', 0, 0, 0, 0, 1),
(839, '提交编辑', 835, 'Take/edit_post', '', '', '', 0, 0, 0, 0, 1),
(840, '删除', 835, 'Take/delete', '', '', '', 0, 0, 0, 0, 1),
(841, '排序', 835, 'Take/setsort', '', '', '', 0, 0, 0, 0, 1),
(842, '设置状态', 835, 'Take/setstatus', '', '', '', 0, 0, 0, 0, 1),
(843, '导出数据', 835, 'Take/export', '', '', '', 0, 0, 0, 0, 1),
(844, 'IP黑名单', 10, 'IpBlacklist/index', '', '', '', 1, 0, 0, 0, 1),
(845, '添加', 844, 'IpBlacklist/add', '', '', '', 0, 0, 0, 0, 1),
(846, '提交添加', 844, 'IpBlacklist/add_post', '', '', '', 0, 0, 0, 0, 1),
(847, '编辑', 844, 'IpBlacklist/edit', '', '', '', 0, 0, 0, 0, 1),
(848, '提交编辑', 844, 'IpBlacklist/edit_post', '', '', '', 0, 0, 0, 0, 1),
(849, '删除', 844, 'IpBlacklist/delete', '', '', '', 0, 0, 0, 0, 1),
(850, '排序', 844, 'IpBlacklist/setsort', '', '', '', 0, 0, 0, 0, 1),
(851, '位置管理', 10, 'Region/index', '', '', '', 1, 0, 0, 0, 1),
(852, '添加', 851, 'Region/add', '', '', '', 0, 0, 0, 0, 1),
(853, '提交添加', 851, 'Region/add_post', '', '', '', 0, 0, 0, 0, 1),
(854, '编辑', 851, 'Region/edit', '', '', '', 0, 0, 0, 0, 1),
(855, '提交编辑', 851, 'Region/edit_post', '', '', '', 0, 0, 0, 0, 1),
(856, '删除', 851, 'Region/delete', '', '', '', 0, 0, 0, 0, 1),
(857, '排序', 851, 'Region/setsort', '', '', '', 0, 0, 0, 0, 1),
(858, '设置状态', 851, 'Region/setstatus', '', '', '', 0, 0, 0, 0, 1),
(867, '基础配置', 1, 'Info/edit?id=1', '', '', '', 1, 1631504485, 1631504548, 0, 1),
(868, '订单管理', 0, 'Order', '', 'fa fa-list', '', 1, 1631514876, 1631514876, 300, 1),
(869, '订单列表', 868, 'Order/index', '', '', '', 1, 0, 0, 0, 1),
(870, '添加', 869, 'Order/add', '', '', '', 0, 0, 0, 0, 1),
(871, '提交添加', 869, 'Order/add_post', '', '', '', 0, 0, 0, 0, 1),
(872, '编辑', 869, 'Order/edit', '', '', '', 0, 0, 0, 0, 1),
(873, '提交编辑', 869, 'Order/edit_post', '', '', '', 0, 0, 0, 0, 1),
(874, '删除', 869, 'Order/delete', '', '', '', 0, 0, 0, 0, 1),
(875, '排序', 869, 'Order/setsort', '', '', '', 0, 0, 0, 0, 1),
(876, '设置状态', 869, 'Order/setstatus', '', '', '', 0, 0, 0, 0, 1);

-- --------------------------------------------------------

--
-- 表的结构 `banner`
--

CREATE TABLE `banner` (
  `id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `sub_title` varchar(500) DEFAULT NULL COMMENT '副标题',
  `brief` varchar(500) DEFAULT NULL,
  `position_id` int(11) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL COMMENT '图片',
  `image_mobi` varchar(500) DEFAULT NULL COMMENT '手机图片',
  `image_pad` varchar(500) DEFAULT NULL COMMENT '平板图片',
  `sort` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `start_time` int(11) UNSIGNED DEFAULT '0' COMMENT '开始时间',
  `end_time` int(11) UNSIGNED DEFAULT '0' COMMENT '结束时间',
  `clicks` int(11) UNSIGNED DEFAULT '0' COMMENT '广告点击数',
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='广告表';

--
-- 转存表中的数据 `banner`
--

INSERT INTO `banner` (`id`, `title`, `sub_title`, `brief`, `position_id`, `link`, `image`, `image_mobi`, `image_pad`, `sort`, `status`, `start_time`, `end_time`, `clicks`, `create_time`, `update_time`) VALUES
(73, '中文01号', '', '', 1, 'http://www.yizhanhongtu.cn', 'https://img2.baidu.com/it/u=2438550738,937998059&fm=26&fmt=auto&gp=0.jpg', '', '', 0, 1, 0, 0, 0, 1570872878, 1571024914);

-- --------------------------------------------------------

--
-- 表的结构 `banner_position`
--

CREATE TABLE `banner_position` (
  `id` int(11) NOT NULL,
  `position_type` varchar(50) DEFAULT '' COMMENT '广告位类型',
  `position_name` varchar(128) DEFAULT NULL COMMENT '名称',
  `position_code` varchar(128) DEFAULT NULL COMMENT '代码',
  `brief` varchar(500) NOT NULL,
  `sort` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  `settings` text,
  `clicks` int(11) UNSIGNED DEFAULT '0' COMMENT '广告位点击数',
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='广告位表';

--
-- 转存表中的数据 `banner_position`
--

INSERT INTO `banner_position` (`id`, `position_type`, `position_name`, `position_code`, `brief`, `sort`, `status`, `settings`, `clicks`, `create_time`, `update_time`) VALUES
(1, 'htmls', '首页轮播cn', 'banner_kv_cn', '中文版首页轮播图', 0, 1, 'left||||0|0', 0, 1465372692, 1553741576);

-- --------------------------------------------------------

--
-- 表的结构 `columns_category`
--

CREATE TABLE `columns_category` (
  `id` int(11) NOT NULL,
  `cate_name` varchar(128) DEFAULT NULL COMMENT '分类名称',
  `sort` int(11) NOT NULL COMMENT '排序',
  `status` tinyint(4) NOT NULL COMMENT '状态',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `update_time` int(11) NOT NULL COMMENT '更新时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='下载分类表';

-- --------------------------------------------------------

--
-- 表的结构 `content_template`
--

CREATE TABLE `content_template` (
  `id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT '',
  `tpl_name` varchar(100) DEFAULT '',
  `remark` varchar(500) DEFAULT '',
  `sort` smallint(6) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='内容模板表';

--
-- 转存表中的数据 `content_template`
--

INSERT INTO `content_template` (`id`, `title`, `tpl_name`, `remark`, `sort`, `status`) VALUES
(1, '默认模板', 'index', '', 0, 1),
(2, '供求信息表单', 'supply_and_demand', '', 0, 1);

-- --------------------------------------------------------

--
-- 表的结构 `email_log`
--

CREATE TABLE `email_log` (
  `id` int(11) NOT NULL,
  `msg_tpl_id` int(11) NOT NULL DEFAULT '0',
  `msg_tpl_code` varchar(50) DEFAULT NULL,
  `token` varchar(100) DEFAULT NULL,
  `email_from` varchar(100) DEFAULT NULL,
  `email_to` varchar(150) DEFAULT NULL,
  `subject` varchar(200) DEFAULT NULL,
  `content` longtext,
  `ip_addr` varchar(20) DEFAULT NULL,
  `ip_info` varchar(150) DEFAULT NULL,
  `result` varchar(2000) DEFAULT NULL,
  `result_msg` varchar(200) DEFAULT NULL,
  `views` int(11) DEFAULT '0',
  `view_ip_addr` varchar(50) DEFAULT '''''',
  `view_ip_info` varchar(50) DEFAULT '''''',
  `view_time` int(11) DEFAULT NULL,
  `lang` varchar(10) DEFAULT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `event_category`
--

CREATE TABLE `event_category` (
  `id` int(11) NOT NULL,
  `cate_name_cn` varchar(150) DEFAULT NULL,
  `cate_name_en` varchar(150) DEFAULT NULL,
  `cate_name_jp` varchar(100) DEFAULT '',
  `tag` varchar(150) DEFAULT NULL,
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='同期活动类型表';

-- --------------------------------------------------------

--
-- 表的结构 `gallery`
--

CREATE TABLE `gallery` (
  `id` int(11) NOT NULL,
  `title_cn` varchar(500) DEFAULT NULL,
  `title_en` varchar(500) DEFAULT NULL,
  `title_jp` varchar(100) DEFAULT '',
  `brief_cn` varchar(500) DEFAULT NULL,
  `brief_en` varchar(500) DEFAULT NULL,
  `brief_jp` varchar(500) DEFAULT '',
  `pid` int(11) NOT NULL DEFAULT '0',
  `category_id` int(11) NOT NULL DEFAULT '0',
  `image` varchar(500) DEFAULT NULL,
  `keywords` varchar(1000) DEFAULT NULL,
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '1',
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='相册表';

-- --------------------------------------------------------

--
-- 表的结构 `idcard_log`
--

CREATE TABLE `idcard_log` (
  `id` int(10) NOT NULL,
  `name` varchar(80) DEFAULT NULL,
  `idcard` varchar(80) DEFAULT NULL,
  `redata` text NOT NULL,
  `create_time` bigint(20) NOT NULL,
  `status` tinyint(2) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `info`
--

CREATE TABLE `info` (
  `id` int(11) NOT NULL,
  `info` text,
  `take` text,
  `stay` text,
  `status` tinyint(2) DEFAULT '1',
  `sort` varchar(10) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `info`
--

INSERT INTO `info` (`id`, `info`, `take`, `stay`, `status`, `sort`, `create_time`) VALUES
(1, '{\"title\":\"\\u2764\\u7ebf\\u4e0a\\u76f2\\u76d2\\u2764\",\"wechat\":\"array_rand\",\"email\":\"admin@1999.gs\",\"man\":\"50\",\"woman\":\"50\",\"poster\":\"4,1,3\",\"num\":\"10\",\"appid\":\"appid\",\"appsecret\":\"appsecret\",\"middleware\":[\"1\",\"3\"],\"content\":\"<p><strong>\\u8fd9\\u662f\\u4e00\\u79cd\\u672a\\u77e5\\u7684\\u4ea4\\u53cb\\u65b9\\u5f0f<\\/strong>\\uff0c\\u6b22\\u8fce\\u6295\\u7a3f~<\\/p>\\r\\n\\r\\n<p>\\u54c8\\u55bd\\uff0c\\u76ee\\u524d&quot;\\u7559\\u4e00\\u4e2a&quot;\\u548c&quot;\\u62bd\\u4e00\\u4e2a&quot;\\u529f\\u80fd\\u4ec5\\u97001\\u5143\\u54e6\\uff0c\\u6bcf\\u4eba\\u6bcf\\u5929\\u4e0d\\u9650\\u5236\\u6b21\\u6570\\u7559\\uff0c\\u8bf7\\u4e0d\\u8981<span class=\\\"red\\\">\\u865a\\u5047\\u6295\\u653e \\u4f1a\\u5c01IP<\\/span>\\u7684\\u54c8~<\\/p>\"}', '{\"title\":\"\\u62bd\\u4e2a\\u5fae\\u4fe1\",\"price_one\":\"1\",\"price_two\":\"5\",\"pay\":\"yes\",\"num\":\"yes\",\"mutual\":\"yes\",\"alert\":\"\\u7f51\\u7edc\\u4ea4\\u53cb\\u9700\\u8c28\\u614e\\uff01\\u7981\\u6b62\\u5927\\u6279\\u91cf\\u53c2\\u4e0e\\\"\\u62bd\\u4e00\\u4e2a\\\"\\u6d3b\\u52a8\\uff0c\\u7981\\u6b62\\u5fae\\u5546\\u3001\\u7535\\u9500\\u3001\\u5f15\\u6d41\\u7b49\\u7c7b\\u4f3c\\u884c\\u4e1a\\u53c2\\u4e0e\\uff0c\\u4e00\\u7ecf\\u53d1\\u73b0\\u6c38\\u4e45\\u5c01\\u7981IP\\u548c\\u53f7\\u7801\\uff0c\\u5fd8\\u6089\\u77e5\\uff01\",\"content\":\"<p>\\u9009\\u62e9\\u5bf9\\u5e94\\u7684\\u5730\\u533a+\\u6027\\u522b+\\u4f60\\u7684\\u5fae\\u4fe1\\u5c31\\u53ef\\u4ee5\\u62bd\\u5566\\uff0c\\u76ee\\u524d\\u666e\\u901a\\u76f2\\u76d2\\u662f1\\u5143\\uff0c\\u6761\\u4ef6\\u76f2\\u76d2\\u662f5\\u5143\\uff0c\\u81ea\\u884c\\u9009\\u62e9~\\u8bf7\\u6089\\u77e5\\uff01<\\/p>\\r\\n\\r\\n<p><span class=\\\"red\\\">\\u73b0\\u5df2\\u5f00\\u901a\\u6bcf\\u4eba\\u6bcf\\u65e5\\u65e0\\u9650\\u62bd\\uff0c\\u8be6\\u60c5\\u70b9\\u51fb\\u5e95\\u90e8[\\u6d77\\u62a5]<\\/span><\\/p>\\r\\n\\r\\n<p>\\u5982\\u6709\\u5f02\\u8bae\\uff0c<a class=\\\"red\\\" href=\\\"\\/about\\\">\\u8bf7\\u70b9\\u6b64\\u8054\\u7cfb\\u5ba2\\u670d<\\/a>\\uff0c\\u8fdb\\u884c\\u5904\\u7406\\uff01<\\/p>\"}', '{\"title\":\"\\u7559\\u4e2a\\u5fae\\u4fe1\",\"price\":\"1\",\"price_two\":\"5\",\"pay\":\"yes\",\"alert\":\"\\u60a8\\u7684IP\\u5730\\u5740\\u4e3a {$ip} \\u8bf7\\u52ff\\u975e\\u6cd5\\u63d0\\u4ea4\\uff0c\\u7981\\u6b62\\u975e\\u6cd5\\u5185\\u5bb9\\u548c\\u5e26\\u6709\\u76ee\\u7684\\u6027\\u4eba\\u5458\\u53c2\\u4e0e\\u6d3b\\u52a8\\uff01\",\"content\":\"<p><span class=\\\"red\\\">\\u4e0a\\u4f20\\u7167\\u7247\\u4f1a\\u88ab\\u9996\\u9875\\u63a8\\u8350\\u54e6<\\/span>\\uff0c\\u586b\\u5199\\u5e74\\u9f84\\u3001\\u661f\\u5ea7\\u7b49\\u4fe1\\u606f\\u5339\\u914d\\u7684\\u8d28\\u91cf\\u4f1a\\u66f4\\u9ad8\\uff0c\\u6b22\\u8fce\\u8e0a\\u8dc3\\u53c2\\u52a0\\uff01<\\/p>\\r\\n\\r\\n<p>\\u63d0\\u4ea4\\u53f7\\u7801\\u524d\\u8bf7\\u68c0\\u67e5\\u662f\\u5426\\u53ef\\u4ee5\\u6b63\\u5e38\\u641c\\u7d22\\uff0c\\u641c\\u4e0d\\u5230\\u7684\\u4f1a\\u88ab\\u6539\\u4e3a\\u5f85\\u5ba1\\u6838\\uff0c\\u8bf7\\u8054\\u7cfb\\u5ba2\\u670d\\u5904\\u7406\\uff01<\\/p>\\r\\n\\r\\n<p>\\u5982\\u6709\\u5f02\\u8bae\\uff0c<a class=\\\"red\\\" href=\\\"\\/about\\\">\\u8bf7\\u70b9\\u6b64\\u8054\\u7cfb\\u5ba2\\u670d<\\/a>\\uff0c\\u8fdb\\u884c\\u5904\\u7406\\uff01<\\/p>\"}', 1, '0', 0);

-- --------------------------------------------------------

--
-- 表的结构 `ip_blacklist`
--

CREATE TABLE `ip_blacklist` (
  `id` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `remarks` varchar(100) DEFAULT NULL COMMENT '备注',
  `sort` int(10) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `lang`
--

CREATE TABLE `lang` (
  `id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL COMMENT '名称',
  `lang_code` varchar(16) DEFAULT NULL COMMENT '语言代号',
  `sort` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL,
  `create_time` int(11) NOT NULL,
  `update_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='语言表';

--
-- 转存表中的数据 `lang`
--

INSERT INTO `lang` (`id`, `title`, `lang_code`, `sort`, `status`, `create_time`, `update_time`) VALUES
(1, '中文', 'cn', 0, 1, 1540526911, 1540526911);

-- --------------------------------------------------------

--
-- 表的结构 `links`
--

CREATE TABLE `links` (
  `id` int(11) NOT NULL,
  `title` varchar(128) DEFAULT NULL COMMENT '名称',
  `title_en` varchar(128) DEFAULT NULL COMMENT '名称',
  `title_jp` varchar(128) DEFAULT NULL COMMENT '名称',
  `url` varchar(500) DEFAULT NULL COMMENT '跳转链接',
  `url_en` varchar(500) DEFAULT NULL COMMENT '跳转链接',
  `url_jp` varchar(255) DEFAULT NULL COMMENT '跳转链接',
  `target` varchar(50) DEFAULT NULL,
  `brief` varchar(500) DEFAULT NULL,
  `brief_en` varchar(500) DEFAULT NULL,
  `brief_jp` varchar(500) DEFAULT NULL,
  `expo_id` int(11) NOT NULL DEFAULT '0',
  `category_id` int(11) NOT NULL DEFAULT '0',
  `clicks` int(11) DEFAULT '0' COMMENT '点击量',
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(4) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `oid` int(10) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='推广链接表';

--
-- 转存表中的数据 `links`
--

INSERT INTO `links` (`id`, `title`, `title_en`, `title_jp`, `url`, `url_en`, `url_jp`, `target`, `brief`, `brief_en`, `brief_jp`, `expo_id`, `category_id`, `clicks`, `sort`, `status`, `create_time`, `oid`) VALUES
(534, '首页', NULL, NULL, 'http://www.baidu.com', NULL, NULL, NULL, '首页banner', NULL, NULL, 0, 8, 5, 0, 1, 1622171146, 0);

-- --------------------------------------------------------

--
-- 表的结构 `links_category`
--

CREATE TABLE `links_category` (
  `id` int(11) NOT NULL,
  `cate_name` varchar(128) NOT NULL,
  `brief` varchar(250) DEFAULT NULL,
  `pid` int(11) NOT NULL DEFAULT '0',
  `sort` smallint(6) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='推广链接分类表';

--
-- 转存表中的数据 `links_category`
--

INSERT INTO `links_category` (`id`, `cate_name`, `brief`, `pid`, `sort`, `status`) VALUES
(8, '测试分类', '测试的分类', 0, 0, 1);

-- --------------------------------------------------------

--
-- 表的结构 `links_click`
--

CREATE TABLE `links_click` (
  `id` int(11) NOT NULL,
  `links_id` int(11) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `visitor_id` int(11) DEFAULT '0',
  `user_count` int(11) DEFAULT '0',
  `visitor_count` int(11) DEFAULT '0',
  `ip_addr` varchar(150) DEFAULT NULL,
  `raw_url` mediumtext,
  `url_referrer` mediumtext,
  `url` varchar(250) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `hour` bigint(20) DEFAULT NULL,
  `minute` bigint(20) DEFAULT NULL,
  `ip_nation` varchar(50) DEFAULT NULL,
  `ip_province` varchar(150) DEFAULT NULL,
  `ip_city` varchar(100) DEFAULT NULL,
  `country` int(11) DEFAULT NULL,
  `province_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `isp` int(11) DEFAULT '0',
  `user_agent` mediumtext,
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `links_click`
--

INSERT INTO `links_click` (`id`, `links_id`, `user_id`, `visitor_id`, `user_count`, `visitor_count`, `ip_addr`, `raw_url`, `url_referrer`, `url`, `year`, `month`, `day`, `hour`, `minute`, `ip_nation`, `ip_province`, `ip_city`, `country`, `province_id`, `city_id`, `isp`, `user_agent`, `create_time`) VALUES
(410468, 534, 0, 0, 0, 0, '127.0.0.1', NULL, NULL, 'http://www.baidu.com', 2021, 202105, 20210528, 2021052811, 202105281108, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 1622171289),
(410469, 534, 0, 0, 0, 0, '127.0.0.1', NULL, NULL, 'http://www.baidu.com', 2021, 202105, 20210528, 2021052811, 202105281108, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 1622171302),
(410470, 534, 0, 0, 0, 0, '127.0.0.1', NULL, NULL, 'http://www.baidu.com', 2021, 202105, 20210528, 2021052811, 202105281108, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 1622171335),
(410471, 534, 0, 0, 0, 0, '127.0.0.1', NULL, NULL, 'http://www.baidu.com', 2021, 202105, 20210528, 2021052811, 202105281108, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 1622171337);

-- --------------------------------------------------------

--
-- 表的结构 `mailer`
--

CREATE TABLE `mailer` (
  `id` int(11) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `type_id` tinyint(4) NOT NULL DEFAULT '0',
  `email` varchar(150) DEFAULT NULL,
  `name_cn` varchar(100) DEFAULT NULL COMMENT '发件人名称',
  `name_en` varchar(100) DEFAULT NULL COMMENT '发件人名称',
  `email_pwd` varchar(150) DEFAULT NULL,
  `reply_email` varchar(150) DEFAULT NULL COMMENT '回复邮箱',
  `reply_name` varchar(150) DEFAULT NULL COMMENT '回复名称',
  `api_url` varchar(200) DEFAULT NULL,
  `api_user` varchar(150) DEFAULT NULL,
  `api_key` varchar(150) DEFAULT NULL,
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `mailer`
--

INSERT INTO `mailer` (`id`, `title`, `type_id`, `email`, `name_cn`, `name_en`, `email_pwd`, `reply_email`, `reply_name`, `api_url`, `api_user`, `api_key`, `sort`, `status`) VALUES
(2, 'SendCloud', 1, 'swopchina@cloud.mds.cn', '名字', 'CR Expo', 'zjwypiepxuoiddcc', 'swopchina@cloud.mds.cn', 'CR Expo', 'http://api.sendcloud.net/apiv2/mail/send', 'poly2019', 'qnUZcq2zCeCwF3f5', 100, 1);

-- --------------------------------------------------------

--
-- 表的结构 `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `menu_name` varchar(128) NOT NULL COMMENT '菜单名称',
  `image` varchar(500) DEFAULT NULL COMMENT '图片',
  `pid` int(11) DEFAULT NULL COMMENT '父级',
  `pathinfo` varchar(128) DEFAULT NULL COMMENT '链接路径',
  `sub_category` varchar(64) DEFAULT NULL COMMENT '下级分类',
  `content_type` int(11) DEFAULT NULL COMMENT '内容类型',
  `content_id` int(11) DEFAULT NULL COMMENT '调用内容页面ID',
  `module_type` varchar(128) DEFAULT NULL COMMENT '模块类型',
  `content_category` int(11) DEFAULT NULL COMMENT '内容分类ID',
  `content_tpl` varchar(100) DEFAULT '' COMMENT '内容模板名称',
  `tpl_name` varchar(128) DEFAULT NULL COMMENT '模板名称',
  `breadcrumb` tinyint(1) NOT NULL DEFAULT '0' COMMENT '面包屑状态',
  `pager_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '分页状态',
  `pager_list_rows` smallint(6) NOT NULL DEFAULT '0' COMMENT '每页数量',
  `sort` int(11) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  `header_status` tinyint(1) NOT NULL DEFAULT '1',
  `footer_status` tinyint(1) NOT NULL DEFAULT '1',
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='前台菜单表';

--
-- 转存表中的数据 `menu`
--

INSERT INTO `menu` (`id`, `menu_name`, `image`, `pid`, `pathinfo`, `sub_category`, `content_type`, `content_id`, `module_type`, `content_category`, `content_tpl`, `tpl_name`, `breadcrumb`, `pager_status`, `pager_list_rows`, `sort`, `status`, `header_status`, `footer_status`, `create_time`, `update_time`) VALUES
(140, '首页', '', 0, '', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622171393, 1622791143),
(141, '关于我们', '', 0, 'about', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622171604, 1622791140),
(142, '新闻中心', '', 0, 'news', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622171631, 1622791109),
(143, '我们的产品', '', 0, 'product', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622171666, 1622791105),
(144, '解决方案', '', 0, 'solution', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622171698, 1622791101),
(145, '联系我们', '/uploads/menu/20210528/7437b1c5847c0c688170523724b2396b.png', 0, 'contact', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622172347, 1622791136),
(160, '行业新闻', '', 142, 'news/industry', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622791009, 1622791118),
(161, '公司新闻', '', 142, 'news/company', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622791033, 1622791124),
(162, '生物试剂', '', 143, 'product/biological-reagent', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622791199, 1622791199),
(163, '实验耗材', '', 143, 'product/experimental-consumables', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622791222, 1622791222),
(164, '仪器设备', '', 143, 'product/Instrument-and-equipment', NULL, 0, 0, '', 0, '', '', 1, 1, 20, 0, 1, 1, 1, 1622791249, 1622791249);

-- --------------------------------------------------------

--
-- 表的结构 `menu_info`
--

CREATE TABLE `menu_info` (
  `id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `lang` varchar(16) NOT NULL COMMENT '语言',
  `title` varchar(500) DEFAULT NULL COMMENT '标题',
  `sub_title` varchar(200) DEFAULT '',
  `name` varchar(256) DEFAULT NULL,
  `brief` varchar(1000) DEFAULT NULL COMMENT '简介',
  `content` longtext COMMENT '内容',
  `image` varchar(150) DEFAULT NULL,
  `outlink` varchar(500) DEFAULT NULL COMMENT '外链',
  `target` varchar(128) DEFAULT NULL COMMENT '打开方式',
  `meta_title` varchar(500) DEFAULT NULL,
  `meta_desc` varchar(500) DEFAULT NULL,
  `meta_kws` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='菜单信息表';

--
-- 转存表中的数据 `menu_info`
--

INSERT INTO `menu_info` (`id`, `menu_id`, `lang`, `title`, `sub_title`, `name`, `brief`, `content`, `image`, `outlink`, `target`, `meta_title`, `meta_desc`, `meta_kws`) VALUES
(193, 140, 'cn', '', '', '首页', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(194, 140, 'en', '', '', '首页', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(195, 141, 'cn', '', '', '关于我们', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(196, 141, 'en', '', '', 'About us', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(197, 142, 'cn', '', '', '新闻中心', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(198, 142, 'en', '', '', 'News Center', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(199, 143, 'cn', '', '', '我们的产品', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(200, 143, 'en', '', '', 'Our products', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(201, 144, 'cn', '', '', '解决方案', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(202, 144, 'en', '', '', 'Solution', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(203, 145, 'cn', '', '', '联系我们', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(204, 145, 'en', '', '', 'contact us', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(205, 146, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(206, 146, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(207, 147, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(208, 147, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(209, 148, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(210, 148, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(211, 149, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(212, 149, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(213, 150, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(214, 150, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(215, 151, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(216, 151, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(217, 152, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(218, 152, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(219, 153, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(220, 153, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(221, 154, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(222, 154, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(223, 155, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(224, 155, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(225, 156, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(226, 156, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(227, 157, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(228, 157, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(229, 158, 'cn', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(230, 158, 'en', '', '', '', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(231, 159, 'cn', '', '', '', '', '<p>中文</p>', NULL, '', '_self', '', '', ''),
(232, 159, 'en', '', '', '', '', '<p>yinwen</p>', NULL, '', '_self', '', '', ''),
(233, 160, 'cn', '', '', '行业新闻', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(234, 160, 'en', '', '', 'Industry news', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(235, 161, 'cn', '', '', '公司新闻', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(236, 161, 'en', '', '', 'Company news', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(237, 162, 'cn', '', '', '生物试剂', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(238, 162, 'en', '', '', 'Biological reagent', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(239, 163, 'cn', '', '', '实验耗材', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(240, 163, 'en', '', '', 'Experimental consumables', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(241, 164, 'cn', '', '', '仪器设备', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', ''),
(242, 164, 'en', '', '', 'Instrument and equipment', '', '<p>&nbsp;</p>', NULL, '', '_self', '', '', '');

-- --------------------------------------------------------

--
-- 表的结构 `msg_template`
--

CREATE TABLE `msg_template` (
  `id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT '1',
  `code` varchar(50) DEFAULT NULL,
  `is_email` int(11) NOT NULL DEFAULT '0',
  `is_sms` int(11) NOT NULL DEFAULT '0',
  `is_msg` int(11) NOT NULL DEFAULT '0',
  `content_tag` varchar(200) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `subject_cn` varchar(200) DEFAULT NULL,
  `subject_en` varchar(200) DEFAULT NULL,
  `email_content_cn` mediumtext,
  `email_content_en` mediumtext,
  `msg_content_cn` varchar(1000) DEFAULT NULL,
  `msg_content_en` varchar(1000) DEFAULT NULL,
  `sms_content_cn` varchar(500) DEFAULT NULL,
  `sms_content_en` varchar(500) DEFAULT NULL,
  `sort` smallint(6) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `update_time` int(11) DEFAULT NULL,
  `bcc` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `news`
--

CREATE TABLE `news` (
  `id` int(11) NOT NULL,
  `title_data` varchar(1000) DEFAULT NULL,
  `category_id` int(11) NOT NULL DEFAULT '0',
  `type_id` tinyint(4) NOT NULL DEFAULT '1' COMMENT '类型1默认2微信',
  `image` varchar(500) DEFAULT NULL,
  `link` varchar(200) DEFAULT '',
  `source_url` varchar(250) DEFAULT NULL COMMENT '来源URL',
  `create_uid` int(11) NOT NULL DEFAULT '0',
  `create_uname` varchar(128) DEFAULT NULL,
  `clicks` int(11) NOT NULL DEFAULT '0',
  `is_top` tinyint(1) NOT NULL DEFAULT '0',
  `is_hot` tinyint(1) NOT NULL DEFAULT '0',
  `is_home` tinyint(1) NOT NULL DEFAULT '0',
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `publish_time` int(11) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新闻主表';

--
-- 转存表中的数据 `news`
--

INSERT INTO `news` (`id`, `title_data`, `category_id`, `type_id`, `image`, `link`, `source_url`, `create_uid`, `create_uname`, `clicks`, `is_top`, `is_hot`, `is_home`, `sort`, `status`, `publish_time`, `create_time`, `update_time`) VALUES
(919, '{\"cn\":\"网站条款\",\"en\":\"title\"}', 7, 1, NULL, '', NULL, 0, NULL, 22, 0, 0, 0, 0, 1, 1631894400, 1622185264, 1631936859);

-- --------------------------------------------------------

--
-- 表的结构 `news_category`
--

CREATE TABLE `news_category` (
  `id` int(11) NOT NULL,
  `cate_name_cn` varchar(128) DEFAULT NULL COMMENT '分类名称',
  `cate_name_en` varchar(128) DEFAULT NULL,
  `cate_name_jp` varchar(100) DEFAULT '',
  `pathinfo` varchar(128) NOT NULL,
  `pid` int(11) NOT NULL DEFAULT '0',
  `image` varchar(500) DEFAULT NULL COMMENT '展示图片',
  `brief_cn` varchar(500) DEFAULT NULL COMMENT '简介',
  `brief_en` varchar(500) DEFAULT NULL,
  `brief_jp` varchar(500) DEFAULT '',
  `is_menu` tinyint(1) NOT NULL DEFAULT '0' COMMENT '菜单中显示',
  `tpl_id` int(11) NOT NULL DEFAULT '0',
  `tpl_name` varchar(128) DEFAULT NULL,
  `sort` int(11) NOT NULL COMMENT '排序',
  `status` tinyint(4) NOT NULL COMMENT '状态',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `update_time` int(11) NOT NULL COMMENT '更新时间',
  `list_status` tinyint(2) DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新闻分类表';

--
-- 转存表中的数据 `news_category`
--

INSERT INTO `news_category` (`id`, `cate_name_cn`, `cate_name_en`, `cate_name_jp`, `pathinfo`, `pid`, `image`, `brief_cn`, `brief_en`, `brief_jp`, `is_menu`, `tpl_id`, `tpl_name`, `sort`, `status`, `create_time`, `update_time`, `list_status`) VALUES
(7, '公告', 'gonggao', '', '', 0, '', '公告', 'gonggao', '', 1, 0, NULL, 0, 1, 1622185221, 1631933846, 1);

-- --------------------------------------------------------

--
-- 表的结构 `news_info`
--

CREATE TABLE `news_info` (
  `id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `lang` varchar(16) NOT NULL,
  `title` varchar(500) DEFAULT NULL COMMENT '标题',
  `sub_title` varchar(500) DEFAULT NULL COMMENT '副标题',
  `image` varchar(200) DEFAULT NULL,
  `brief` text COMMENT '简介',
  `content` mediumtext COMMENT '内容',
  `author` varchar(128) DEFAULT NULL COMMENT '作者',
  `source` varchar(128) DEFAULT NULL COMMENT '来源',
  `outlink` varchar(500) DEFAULT NULL COMMENT '外链接',
  `clicks` int(11) NOT NULL DEFAULT '0',
  `meta_title` varchar(500) DEFAULT NULL,
  `meta_desc` varchar(500) DEFAULT NULL,
  `meta_kws` varchar(1000) DEFAULT NULL,
  `info_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新闻信息表';

--
-- 转存表中的数据 `news_info`
--

INSERT INTO `news_info` (`id`, `news_id`, `lang`, `title`, `sub_title`, `image`, `brief`, `content`, `author`, `source`, `outlink`, `clicks`, `meta_title`, `meta_desc`, `meta_kws`, `info_status`) VALUES
(2297, 919, 'cn', '网站条款', '', '/uploads/news/20210528/99071e3296ecb75044790084eecd90c0.png', '', '<p><span style=\"font-size:16px\"><strong>一、用户协议</strong></span></p>\r\n\r\n<p>1、我们善意的提醒您，请仔细阅读本站全部条款，避免发生责任纠纷、隐私争议和相关法律问题；</p>\r\n\r\n<p>2、本站不存在注册和登录功能，不会越权获取非用户主动填写的数据；</p>\r\n\r\n<p>3、支付由微信官方提供，一切支付、退款记录均以微信官方提供记录为准；</p>\r\n\r\n<p>4、我们竭尽全力通过合理有效的技术手段，防止您的信息泄露、损毁、丢失，会按照&quot;隐私条款&quot;中规定进行收集、使用、保存、共享您的个人信息；</p>\r\n\r\n<p>5、我们会对站内数据、用户等数据，不定期做出抽查，有权对不良用户和数据进行清退；</p>\r\n\r\n<p>6、因技术局限性，我们会尽力保障系统安全稳定运行，但是不排除因不可抗力、黑客攻击、网络中断、政府行为等原因，均有可能造成我站的服务中断、数据丢失以及其他损失或风险；</p>\r\n\r\n<p>7、提交信息即代表同意本站将您所提交的所有信息用于信息发布、提供他人抽取、共享等服务；</p>\r\n\r\n<p>8、用户使用本站功能后所取得的信息需自行辨别真假，不要盲目交友，网络交友需谨慎；</p>\r\n\r\n<p>9、本站仅提供信息收集、发布、共享等服务，用户在离开本站后所发生的任何问题本站将不会承担法律责任，包括但不限于线下约会、交易纠纷等问题，请悉知；</p>\r\n\r\n<hr />\r\n<p><span style=\"font-size:16px\"><strong>二、隐私条款</strong></span></p>\r\n\r\n<p>1、为了向您和其他用户提供更好的服务，我们仅收集必要的信息，其他信息用户可自主选择填写；</p>\r\n\r\n<p>2、提交信息既代表您同意了本站的用户协议、隐私条款、行为规范等条款和规范；</p>\r\n\r\n<p>3、我们将您所提交的个人信息存至数据库，除本站特有功能外，不会对外透漏；</p>\r\n\r\n<p>4、提交信息既代表您同意将您所提交的信息供他人抽取，并且所造成的任何问题由您个人承担；</p>\r\n\r\n<hr />\r\n<p><span style=\"font-size:16px\"><strong>三、行为规范</strong></span></p>\r\n\r\n<p>1、禁止18岁以下未成年人参与本站任何活动；</p>\r\n\r\n<p>2、禁止发布违反国家法律相关的文字、图片、视频等信息；</p>\r\n\r\n<p>3、禁止发布违反社会公德、违反道德伦理的不正当言论和行为；</p>\r\n\r\n<p>4、禁止发布带有性暗示、性挑逗等易使人联想的内容；</p>\r\n\r\n<p>5、禁止发布涉及明星绯闻、娱乐八卦、时政新闻等相关内容；</p>\r\n\r\n<p>6、禁止地域黑、恶意调侃、侮辱性描述等行为；</p>\r\n\r\n<p>7、禁止无端指责平台、谩骂、因使用体验导致的恶意吐槽；</p>\r\n\r\n<p>8、禁止借助本站名义，对外发布任何不实言论；</p>\r\n\r\n<p><strong>注意：违反以上任何规定本站将有权对信息进行直接处理，并记录IP和配合相关部门调查处理，其中所造成的法律问题、道德公德问题、站点损失由用户个人负责；</strong></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p style=\"text-align:right\"><strong>2021年9月18日</strong></p>\r\n\r\n<p style=\"text-align:right\"><strong>本条款自发布之日起生效</strong></p>\r\n\r\n<p>&nbsp;</p>', '管理员', '', '', 0, '', '', '', 0),
(2298, 919, 'en', 'title', '', '/uploads/news/20210528/a1bd1a3588d74b56aaca2df8ddf051e0.png', '', '<p>content</p>', '', '', '', 0, '', '', '', 0);

-- --------------------------------------------------------

--
-- 表的结构 `order`
--

CREATE TABLE `order` (
  `id` int(11) NOT NULL,
  `order_sn` varchar(50) NOT NULL,
  `data` text NOT NULL,
  `price` varchar(10) NOT NULL,
  `pay_sn` varchar(50) DEFAULT NULL COMMENT '微信支付单号',
  `type` tinyint(2) DEFAULT NULL COMMENT '1偷盲盒 2普通盲盒 3条件盲盒',
  `position` int(10) DEFAULT NULL COMMENT '所属位置',
  `invitation` varchar(10) DEFAULT '0' COMMENT '邀请人',
  `status` tinyint(2) DEFAULT '1' COMMENT '1待付款 2已付款',
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `order`
--

INSERT INTO `order` (`id`, `order_sn`, `data`, `price`, `pay_sn`, `type`, `position`, `invitation`, `status`, `create_time`) VALUES
(69, '2021092616411505104', '{\"province\":\"1\",\"city\":\"2\",\"sex\":\"1\",\"wechat\":\"155566\",\"age\":\"23\",\"constellation\":\"\",\"content\":\"\",\"headimg\":\"\",\"ip\":\"112.96.192.41\",\"paystatus\":1,\"status\":1}', '1', NULL, 1, 1, '0', 1, 1632645675),
(70, '2021092621393117675', '{\"province\":\"1\",\"city\":\"2\",\"sex\":\"2\",\"wechat\":\"jsjsjs\",\"age\":\"19\",\"type\":\"1\",\"constellation\":\"\\u5929\\u79e4\\u5ea7\",\"content\":\"jsjdjs\",\"headimg\":\"\",\"ip\":\"60.73.82.7\",\"paystatus\":1,\"status\":1}', '5', NULL, 1, 1, '0', 1, 1632663571);

-- --------------------------------------------------------

--
-- 表的结构 `page_category`
--

CREATE TABLE `page_category` (
  `id` int(11) NOT NULL,
  `cate_name` varchar(100) DEFAULT '',
  `tpl_id` int(11) NOT NULL DEFAULT '0',
  `sort` smallint(6) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='单语文章分类表';

-- --------------------------------------------------------

--
-- 表的结构 `partner`
--

CREATE TABLE `partner` (
  `id` int(11) NOT NULL,
  `title_cn` varchar(1002) DEFAULT '',
  `title_en` varchar(200) DEFAULT '',
  `title_jp` varchar(200) DEFAULT '',
  `category_id` int(11) NOT NULL DEFAULT '0',
  `link` varchar(500) DEFAULT NULL,
  `brief_cn` varchar(500) DEFAULT NULL,
  `brief_en` varchar(500) DEFAULT NULL,
  `brief_jp` varchar(500) DEFAULT '',
  `image` varchar(500) DEFAULT NULL,
  `sort` int(11) NOT NULL DEFAULT '0',
  `status` int(11) NOT NULL DEFAULT '1',
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合作伙伴表信息表';

--
-- 转存表中的数据 `partner`
--

INSERT INTO `partner` (`id`, `title_cn`, `title_en`, `title_jp`, `category_id`, `link`, `brief_cn`, `brief_en`, `brief_jp`, `image`, `sort`, `status`, `create_time`, `update_time`) VALUES
(342, '中新网', 'chinanews', '', 3, '', '', '', '', '/uploads/partner/20210528/7b6d83885f52212c57bf2876f322ee18.jpg', 0, 1, 1622173766, 1622173766);

-- --------------------------------------------------------

--
-- 表的结构 `partner_category`
--

CREATE TABLE `partner_category` (
  `id` int(11) NOT NULL,
  `cate_name_cn` varchar(128) DEFAULT NULL COMMENT '分类名称',
  `cate_name_en` varchar(128) DEFAULT NULL,
  `sort` int(11) NOT NULL COMMENT '排序',
  `status` tinyint(4) NOT NULL COMMENT '状态',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `update_time` int(11) NOT NULL COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合作伙伴分类表';

--
-- 转存表中的数据 `partner_category`
--

INSERT INTO `partner_category` (`id`, `cate_name_cn`, `cate_name_en`, `sort`, `status`, `create_time`, `update_time`) VALUES
(3, '媒体合作', 'Media cooperation', 0, 1, 1622173723, 1622173723);

-- --------------------------------------------------------

--
-- 表的结构 `region`
--

CREATE TABLE `region` (
  `id` int(11) UNSIGNED NOT NULL,
  `name_cn` varchar(100) NOT NULL,
  `name_en` varchar(100) NOT NULL,
  `pid` int(11) UNSIGNED NOT NULL,
  `path` varchar(100) DEFAULT NULL,
  `grade` varchar(100) DEFAULT NULL,
  `pinyin` varchar(100) DEFAULT NULL,
  `sort` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `is_system` tinyint(1) DEFAULT '0',
  `area_group_id` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `region`
--

INSERT INTO `region` (`id`, `name_cn`, `name_en`, `pid`, `path`, `grade`, `pinyin`, `sort`, `status`, `is_system`, `area_group_id`) VALUES
(1, '长春大学', 'changchundaxue', 0, '1,', '1', 'hei gong cheng', '0', 1, 1, 5),
(2, '主校区', 'hljgcxyzxc', 1, '1,2,', '2', 'hei gong cheng zhu xiao qu', '0', 1, 1, 0);

-- --------------------------------------------------------

--
-- 表的结构 `siteinfo`
--

CREATE TABLE `siteinfo` (
  `id` int(11) NOT NULL,
  `config_name` varchar(128) NOT NULL,
  `config_value` mediumtext,
  `title` varchar(128) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `siteinfo`
--

INSERT INTO `siteinfo` (`id`, `config_name`, `config_value`, `title`, `remark`, `status`) VALUES
(1, 'meta_title_cn', '脱单盲盒刀客源码网 - 线上免费盲盒交友', '网站标题（中文）', '', 1),
(2, 'meta_desc_cn', '线上免费脱单盲盒，不限地区，网络一线牵，珍惜这段缘！', '网站描述（中文）', '', 1),
(3, 'meta_kws_cn', '脱单盲盒,刀客源码网,线上脱单盲盒,相亲找对象,线上相亲,免费脱单盲盒', '网站关键字（中文）', '', 1),
(4, 'icp', '黑ICP备2021003744号-1', '网站备案号', '', 1),
(5, 'copyright', '2013-2020 ©刀客源码网', '网站版权', '', 1),
(6, 'tongji', '<script type=\"text/javascript\" src=\"https://v1.cnzz.com/z_stat.php?id=1280317451&web_id=1280317451\"></script>', '网站统计', '统计代码，包括百度、CNZZ等平台的统计代码。', 1),
(7, 'meta_title_en', 'Online free single blind box', '网站标题（英文）', '', 1),
(8, 'meta_desc_en', 'Take off the single blind box online for free, not limited to regions, network first-line lead, cherish this edge!', '网站描述（英文）', '', 1),
(9, 'meta_kws_en', 'Take off single blind box, free blind box, online take off single blind box, blind date finding object, online blind date, free take off single blind box', '网站关键字（英文）', '', 1),
(10, 'black_words', '博彩, 六合彩, 赔率, 高频彩, 赌博, 毒品, 老虎机', '敏感词黑名单', 'etst', 1),
(16, 'smart_title', '后台中心', '后台名称', NULL, 1),
(18, 'google_authenticator', 'LFNTZJ5EGHSQRLMO', '谷歌令牌secret', '安卓验证器下载地址https://share.weiyun.com/Wieb2pGq', 0);

-- --------------------------------------------------------

--
-- 表的结构 `sms_log`
--

CREATE TABLE `sms_log` (
  `id` int(11) NOT NULL,
  `provider` varchar(50) DEFAULT NULL,
  `mobile` varchar(50) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `result` varchar(500) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `ip_addr` varchar(20) DEFAULT NULL,
  `ip_info` varchar(150) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `stay`
--

CREATE TABLE `stay` (
  `id` int(11) NOT NULL,
  `sex` tinyint(2) DEFAULT NULL,
  `province` int(10) DEFAULT '0',
  `city` int(10) DEFAULT '0',
  `wechat` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '微信',
  `content` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `headimg` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '头像',
  `constellation` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '星座',
  `age` int(10) DEFAULT '0' COMMENT '年龄',
  `source` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',
  `ip` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sort` int(11) DEFAULT '0',
  `status` tinyint(2) DEFAULT '1' COMMENT '状态',
  `paystatus` tinyint(2) DEFAULT NULL COMMENT '支付状态1已付款，2未付款，3免费',
  `create_time` int(11) DEFAULT NULL,
  `type` int(2) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `stay`
--

INSERT INTO `stay` (`id`, `sex`, `province`, `city`, `wechat`, `content`, `headimg`, `constellation`, `age`, `source`, `ip`, `sort`, `status`, `paystatus`, `create_time`, `type`) VALUES
(234, 2, 1, 2, '123456', '', '', '', 23, NULL, '61.140.182.211', 0, 1, 3, 1632143040, 0),
(233, 1, 1, 2, '42463987', '', '', '', 23, NULL, '61.140.182.211', 0, 1, 3, 1632143010, 0);

-- --------------------------------------------------------

--
-- 表的结构 `take`
--

CREATE TABLE `take` (
  `id` int(11) NOT NULL,
  `type` tinyint(2) DEFAULT NULL COMMENT '类型：1普通，2高级',
  `data` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '用户提交数据',
  `sid` int(11) DEFAULT NULL COMMENT 'stay表的ID',
  `status` tinyint(2) DEFAULT '1' COMMENT '状态',
  `date` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '日期',
  `wechat` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '抽的人微信',
  `ip` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `paystatus` tinyint(2) DEFAULT NULL COMMENT '支付状态1已付款，2未付款，3免费',
  `invitation_total` int(20) DEFAULT '0' COMMENT '邀请总数',
  `invitation_num` int(20) DEFAULT '0' COMMENT '剩余可抽数',
  `sort` int(11) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 转存表中的数据 `take`
--

INSERT INTO `take` (`id`, `type`, `data`, `sid`, `status`, `date`, `wechat`, `ip`, `paystatus`, `invitation_total`, `invitation_num`, `sort`, `create_time`) VALUES
(142, 1, '{\"province\":\"1\",\"city\":\"2\",\"sex\":\"2\",\"type\":\"1\",\"wechat\":\"42463987\",\"constellation\":\"\",\"headimg\":\"1\",\"age_min\":\"\",\"age_max\":\"\"}', 234, 1, '2021-09-20', '42463987', '61.140.182.211', 3, 0, 0, NULL, 1632143053);

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `account` varchar(64) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL,
  `mobile` varchar(32) NOT NULL,
  `group_id` smallint(6) DEFAULT '0',
  `is_super` tinyint(1) DEFAULT '0' COMMENT '超级管理员',
  `last_login_time` int(11) DEFAULT '0' COMMENT '最后登录时间',
  `last_login_ip` varchar(15) DEFAULT NULL COMMENT '最后登录IP',
  `login_count` smallint(6) DEFAULT '0' COMMENT '登录次数',
  `status` tinyint(1) NOT NULL,
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `update_time` int(11) NOT NULL,
  `province` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `account`, `password`, `email`, `mobile`, `group_id`, `is_super`, `last_login_time`, `last_login_ip`, `login_count`, `status`, `create_time`, `update_time`, `province`) VALUES
(2, 'administrator', '$2y$10$vsYA9V/FVuuqRpMs92voC.4TWlji9dA7G9yu9crfv8zO3X0lEBkAi', 'hljshlx@foxmail.com', '13145214524', 1, 1, 1632712205, '116.21.13.227', 844, 1, 1401359163, 1632712238, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `user_log`
--

CREATE TABLE `user_log` (
  `id` int(10) NOT NULL COMMENT '自增长id',
  `user_id` int(10) NOT NULL COMMENT '管理员id',
  `user_name` varchar(120) DEFAULT NULL COMMENT '管理员名',
  `time` int(11) DEFAULT NULL COMMENT '操作时间',
  `ip` varchar(80) DEFAULT NULL COMMENT 'ip地址',
  `ipinfo` varchar(300) DEFAULT NULL COMMENT 'ip详情',
  `url` varchar(300) DEFAULT '',
  `action` varchar(100) DEFAULT NULL COMMENT '方法名',
  `action_type` varchar(100) DEFAULT NULL COMMENT '操作类型',
  `text` varchar(300) DEFAULT NULL COMMENT '内容',
  `change_id` varchar(300) DEFAULT NULL COMMENT '修改的id',
  `data` text COMMENT '操作数据',
  `create_time` int(11) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `asset`
--
ALTER TABLE `asset`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group_access`
--
ALTER TABLE `auth_group_access`
  ADD UNIQUE KEY `uid_group_id` (`uid`,`group_id`),
  ADD KEY `uid` (`uid`),
  ADD KEY `group_id` (`group_id`);

--
-- Indexes for table `auth_rule`
--
ALTER TABLE `auth_rule`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `name` (`name`) USING BTREE;

--
-- Indexes for table `banner`
--
ALTER TABLE `banner`
  ADD PRIMARY KEY (`id`),
  ADD KEY `position_id` (`position_id`);

--
-- Indexes for table `banner_position`
--
ALTER TABLE `banner_position`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `columns_category`
--
ALTER TABLE `columns_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `content_template`
--
ALTER TABLE `content_template`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `email_log`
--
ALTER TABLE `email_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event_category`
--
ALTER TABLE `event_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gallery`
--
ALTER TABLE `gallery`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `idcard_log`
--
ALTER TABLE `idcard_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `info`
--
ALTER TABLE `info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ip_blacklist`
--
ALTER TABLE `ip_blacklist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ip` (`ip`) USING BTREE;

--
-- Indexes for table `lang`
--
ALTER TABLE `lang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `links`
--
ALTER TABLE `links`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `expo_id` (`expo_id`);

--
-- Indexes for table `links_category`
--
ALTER TABLE `links_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `links_click`
--
ALTER TABLE `links_click`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mailer`
--
ALTER TABLE `mailer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_info`
--
ALTER TABLE `menu_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- Indexes for table `msg_template`
--
ALTER TABLE `msg_template`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `news_category`
--
ALTER TABLE `news_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pid` (`pid`),
  ADD KEY `pathinfo` (`pathinfo`);

--
-- Indexes for table `news_info`
--
ALTER TABLE `news_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `news_id` (`news_id`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `zuhe` (`order_sn`,`position`,`status`) USING BTREE;

--
-- Indexes for table `page_category`
--
ALTER TABLE `page_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner`
--
ALTER TABLE `partner`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `partner_category`
--
ALTER TABLE `partner_category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index` (`pid`);

--
-- Indexes for table `siteinfo`
--
ALTER TABLE `siteinfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `config_name` (`config_name`);

--
-- Indexes for table `sms_log`
--
ALTER TABLE `sms_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stay`
--
ALTER TABLE `stay`
  ADD PRIMARY KEY (`id`),
  ADD KEY `zuhe` (`sex`,`province`,`city`,`wechat`) USING BTREE;

--
-- Indexes for table `take`
--
ALTER TABLE `take`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `account` (`account`);

--
-- Indexes for table `user_log`
--
ALTER TABLE `user_log`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `asset`
--
ALTER TABLE `asset`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `auth_rule`
--
ALTER TABLE `auth_rule`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=877;

--
-- 使用表AUTO_INCREMENT `banner`
--
ALTER TABLE `banner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- 使用表AUTO_INCREMENT `banner_position`
--
ALTER TABLE `banner_position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `columns_category`
--
ALTER TABLE `columns_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `content_template`
--
ALTER TABLE `content_template`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `email_log`
--
ALTER TABLE `email_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `event_category`
--
ALTER TABLE `event_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `gallery`
--
ALTER TABLE `gallery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `idcard_log`
--
ALTER TABLE `idcard_log`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- 使用表AUTO_INCREMENT `info`
--
ALTER TABLE `info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用表AUTO_INCREMENT `ip_blacklist`
--
ALTER TABLE `ip_blacklist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用表AUTO_INCREMENT `lang`
--
ALTER TABLE `lang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `links`
--
ALTER TABLE `links`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=535;

--
-- 使用表AUTO_INCREMENT `links_category`
--
ALTER TABLE `links_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用表AUTO_INCREMENT `links_click`
--
ALTER TABLE `links_click`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=410472;

--
-- 使用表AUTO_INCREMENT `mailer`
--
ALTER TABLE `mailer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=165;

--
-- 使用表AUTO_INCREMENT `menu_info`
--
ALTER TABLE `menu_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=243;

--
-- 使用表AUTO_INCREMENT `msg_template`
--
ALTER TABLE `msg_template`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用表AUTO_INCREMENT `news`
--
ALTER TABLE `news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=920;

--
-- 使用表AUTO_INCREMENT `news_category`
--
ALTER TABLE `news_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用表AUTO_INCREMENT `news_info`
--
ALTER TABLE `news_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2299;

--
-- 使用表AUTO_INCREMENT `order`
--
ALTER TABLE `order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- 使用表AUTO_INCREMENT `page_category`
--
ALTER TABLE `page_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `partner`
--
ALTER TABLE `partner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=343;

--
-- 使用表AUTO_INCREMENT `partner_category`
--
ALTER TABLE `partner_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用表AUTO_INCREMENT `region`
--
ALTER TABLE `region`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3846;

--
-- 使用表AUTO_INCREMENT `siteinfo`
--
ALTER TABLE `siteinfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- 使用表AUTO_INCREMENT `sms_log`
--
ALTER TABLE `sms_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `stay`
--
ALTER TABLE `stay`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=235;

--
-- 使用表AUTO_INCREMENT `take`
--
ALTER TABLE `take`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143;

--
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `user_log`
--
ALTER TABLE `user_log`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '自增长id';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
