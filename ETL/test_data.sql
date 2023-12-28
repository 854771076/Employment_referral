INSERT INTO `jobfree`.`user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `has_resume`, `last_update`) VALUES (1, 'pbkdf2_sha256$260000$R8vGws1zEFAPVTqDlX517K$ndi59BtPgKB6SrE4TNaXnYXpeV9VYzTB7X9w+dj/Po4=', NULL, 1, 'root', '', '', '854771076@qq.com', 1, 1, '2023-10-20 09:37:58.835221', '', 1, '2023-10-20 09:37:58.957336');
INSERT INTO `jobfree`.`user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `has_resume`, `last_update`) VALUES (2, 'pbkdf2_sha256$260000$R8vGws1zEFAPVTqDlX517K$ndi59BtPgKB6SrE4TNaXnYXpeV9VYzTB7X9w+dj/Po4=', NULL, 1, 'JF100000', '', '', '2910226625@qq.com', 1, 1, '2023-10-20 09:37:58.835221', '', 1, '2023-10-20 09:37:58.957336');
INSERT INTO `jobfree`.`user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`, `has_resume`, `last_update`) VALUES (3, 'pbkdf2_sha256$260000$R8vGws1zEFAPVTqDlX517K$ndi59BtPgKB6SrE4TNaXnYXpeV9VYzTB7X9w+dj/Po4=', NULL, 1, 'JF100001', '', '', 'fuyang854771076@gmail.com', 1, 1, '2023-10-20 09:37:58.835221', '', 1, '2023-10-20 09:37:58.957336');

INSERT INTO `jobfree`.`resume` (`id`, `eduHighestLevel`, `eduHighestLevelTranslation`, `workingexpCode`, `workingexp`, `worktypeCode`, `worktype`, `workcity`, `workcityTranslation`, `workcity2`, `workcity2Translation`, `workcity3`, `workcity3Translation`, `subjobtypelevel`, `subjobtypelevelname`, `skilllabel`, `propertycode`, `property`, `preferredSalaryMin`, `preferredSalaryMax`, `SelfEvaluate`, `created_time`, `last_update`, `user_id`) VALUES (5, 5, '本科', 1, '1年以下', 2, '全职', 530, '北京', 0, NULL, 0, NULL, 9000300040000, 'C++', 'C++/Java/Python', 5, '民营企业', 10000, 20000, '具备良好的团队合作精神。', '2023-10-19 16:14:48.701070', '2023-10-20 16:14:48.000000', 1);
INSERT INTO `jobfree`.`resume` (`id`, `eduHighestLevel`, `eduHighestLevelTranslation`, `workingexpCode`, `workingexp`, `worktypeCode`, `worktype`, `workcity`, `workcityTranslation`, `workcity2`, `workcity2Translation`, `workcity3`, `workcity3Translation`, `subjobtypelevel`, `subjobtypelevelname`, `skilllabel`, `propertycode`, `property`, `preferredSalaryMin`, `preferredSalaryMax`, `SelfEvaluate`, `created_time`, `last_update`, `user_id`) VALUES (6, 5, '本科', 0, '无经验', 3, '实习', 530, '北京', 570, '保定', 566, '唐山', 7000200170000, '工程造价', 'C++/Java/Python', 5, '民营企业', 1000, 5000, '具备良好的团队合作精神。', '2023-10-19 16:14:48.701070', '2023-10-20 16:14:48.000000', 2);
INSERT INTO `jobfree`.`resume` (`id`, `eduHighestLevel`, `eduHighestLevelTranslation`, `workingexpCode`, `workingexp`, `worktypeCode`, `worktype`, `workcity`, `workcityTranslation`, `workcity2`, `workcity2Translation`, `workcity3`, `workcity3Translation`, `subjobtypelevel`, `subjobtypelevelname`, `skilllabel`, `propertycode`, `property`, `preferredSalaryMin`, `preferredSalaryMax`, `SelfEvaluate`, `created_time`, `last_update`, `user_id`) VALUES (7, 5, '本科', 1, '1年以下', 1, '兼职/临时', 530, '北京', 570, '保定', 566, '唐山', 14000600100000, '后勤', 'C++/Java/Python', 5, '民营企业', 3000, 6000, '具备良好的团队合作精神。', '2023-10-19 16:14:48.701070', '2023-10-20 16:14:48.000000', 3);


INSERT INTO `jobfree`.`starjobs` (`create_time`, `job_id`, `user_id`) VALUES ( '2023-10-23 17:45:03', 1, 1);

INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 2, 1);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 3, 1);

INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 4, 1);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 2, 2);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 44, 2);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 55, 2);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 66, 2);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 2, 3);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 23, 3);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 25, 3);
INSERT INTO `jobfree`.`starjobs` ( `create_time`, `job_id`, `user_id`) VALUES ('2023-10-23 17:45:03', 26, 3);


INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 1, 1, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`, `user_id`, `job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 1, 2, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`,  `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 1, 3, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`,  `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 1, 4, '2023-10-27 09:17:27.000000');

INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`,`last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 2, 11, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`, `user_id`, `job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 2, 12, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 2, 13, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 2, 14, '2023-10-27 09:17:27.000000');

INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 3, 21, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`, `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 3, 22, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`,  `user_id`,`job_id`,  `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 3, 23, '2023-10-27 09:17:27.000000');
INSERT INTO `jobfree`.`clickjobs` (`count`, `create_time`, `user_id`, `job_id`,  `last_update`) VALUES ( 10, '2023-10-27 09:17:18.000000', 3, 24, '2023-10-27 09:17:27.000000');