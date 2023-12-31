create database ods_jobfree;
create database dwd_jobfree;
create database ads_jobfree;
drop table `ods_jobfree.ods_jobfree_db_jobfree_t_resume`;
drop table `ods_jobfree.ods_jobfree_db_spider_t_jobs`;

drop table `dwd_jobfree.dwd_jobfree_db_jobfree_t_resume`;
drop table `dwd_jobfree.dwd_jobfree_db_jobfree_t_resume_train`;
drop table `dwd_jobfree.dwd_jobfree_db_spider_t_jobs`;
drop table `dwd_jobfree.dwd_jobfree_db_spider_t_jobs_train`;
drop table `dwd_jobfree.dwd_jobfree_db_spider_t_company`;

drop table `ads_jobfree.ads_jobfree_db_jobfree_t_recommendforallusers`

create database ods_jobfree;

CREATE TABLE `ods_jobfree`.`ods_jobfree_db_spider_t_jobs` (
  `job_id` int,
  `abroadFlag` string ,
  `abroadTipInfo` string ,
  `alreadyCallPhone` string ,
  `applyType` string ,
  `campusBestCompany` string ,
  `campusRootOrgInfo` string ,
  `canBeRegular` string ,
  `canRemoteInternship` string ,
  `cardCustomJson` string ,
  `cardType` string ,
  `chatWindow` string ,
  `cityDistrict` string ,
  `cityId` string ,
  `companyId` string ,
  `companyLogo` string ,
  `companyName` string ,
  `companyNumber` string ,
  `companyRootId` string ,
  `companyScaleTypeTagsNew` string ,
  `companySize` string ,
  `companyUrl` string ,
  `deliveryPath` string ,
  `displayPhoneNumber` string ,
  `distance` string ,
  `distanceFormat` string ,
  `education` string ,
  `extensions` string ,
  `featureServer` string ,
  `feedOperation` string ,
  `feedPosition` string ,
  `financingStage` string ,
  `firstPublishTime` string ,
  `hasAppliedPosition` string ,
  `industryCompanyTags` string ,
  `industryName` string ,
  `internshipMonths` string ,
  `isNewPosition` string ,
  `jobId` string ,
  `jobSummary` string ,
  `liveCard` string ,
  `matchInfo` string ,
  `menVipLevel` string ,
  `name` string ,
  `needMajor` string ,
  `number` string ,
  `orgBestEmployerFlag` string ,
  `orgPayedFlag` string ,
  `organizer` string ,
  `positionCommercialLabel` string ,
  `positionExpandCardData` string ,
  `positionExpandCardType` string ,
  `positionHighlight` string ,
  `positionOfNlp` string ,
  `positionSourceType` string ,
  `positionSourceTypeUrl` string ,
  `positionUrl` string ,
  `property` string ,
  `propertyCode` string ,
  `propertyType` string ,
  `propertyTypeUrl` string ,
  `provideInternshipCertificate` string ,
  `proxyModel` string ,
  `publishTime` string ,
  `recallSign` string ,
  `recruitNumber` string ,
  `redirectUrl` string ,
  `redirectable` string ,
  `rootCompanyNumber` string ,
  `rpoProxied` string ,
  `rpoProxy` string ,
  `salary60` string ,
  `salaryCount` string ,
  `salaryReal` string ,
  `salaryType` string ,
  `settlementType` string ,
  `showDistance` string ,
  `skillLabel` string ,
  `skillLabelPersonality` string ,
  `staffCard` string ,
  `streetId` string ,
  `streetName` string ,
  `subJobTypeLevel` string ,
  `subJobTypeLevelName` string ,
  `tagABC` string ,
  `tradingArea` string ,
  `volcanoMeterial` string ,
  `weeklyInternshipDays` string ,
  `welfareLabel` string ,
  `welfareTagList` string ,
  `workCity` string ,
  `workDateType` string ,
  `workMode` string ,
  `workType` string ,
  `workingExp` string ,
  `local_row_update_time` timestamp,
  `cdc_sync_date` timestamp
) PARTITIONED BY (partition_date string);
CREATE TABLE `ods_jobfree`.`ods_jobfree_db_jobfree_t_resume` (
  `id` string,
  `eduHighestLevel` int,
  `eduHighestLevelTranslation` string,
  `workingexpCode` int,
  `workingexp` string,
  `worktypeCode` int,
  `worktype` string,
  `workcity` int,
  `workcityTranslation` string,
  `workcity2` int,
  `workcity2Translation` string,
  `workcity3` int,
  `workcity3Translation` string,
  `subjobtypelevel` bigint,
  `subjobtypelevelname` string,
  `skilllabel` string,
  `propertycode` int,
  `property` string,
  `preferredSalaryMin` int,
  `preferredSalaryMax` int,
  `SelfEvaluate` string,
  `created_time` timestamp,
  `last_update` timestamp,
  `user_id` int,
  `cdc_sync_date` timestamp
) PARTITIONED BY (partition_date string);

CREATE TABLE `ods_jobfree`.`ods_jobfree_db_jobfree_t_clickjobs` (
  `cid` string,
  `count` int,
  `created_time` timestamp,
  `last_update` timestamp,
  `job_id` int,
  `user_id` int,
  `cdc_sync_date` timestamp
) PARTITIONED BY (partition_date string);

CREATE TABLE `ods_jobfree`.`ods_jobfree_db_jobfree_t_starjobs` (
  `sid` string,
  `created_time` timestamp,
  `job_id` int,
  `user_id` int,
  `cdc_sync_date` timestamp
) PARTITIONED BY (partition_date string);
CREATE TABLE `dwd_jobfree.dwd_jobfree_db_jobfree_t_hotjobs`(	
  `job_id` string, 	
  `weight` bigint
  )	PARTITIONED BY (partition_date string);
CREATE TABLE `dwd_jobfree.dwd_jobfree_db_spider_t_jobs`(
`job_id` int,
`jobid` string, 
`number` string, 
`name` string,
`educationCode` int, 
`education` string, 
`industrycompanytags` string, 
`industryname` string, 
`jobsummary` string, 
`positionurl` string, 
`positionsourcetypeurl` string, 
`property` string, 
`propertycode` int, 
`recruitnumber` string, 
`salary60` string, 
`salaryreal` string, 
`salary_min` int,
`salary_max` int,
`salarytype` string, 
`salarycounte` string, 
`skilllabel` string, 
`publishtime` timestamp, 
`citydistrict` string, 
`streetid` string, 
`streetname` string, 
`subjobtypelevel` BIGINT, 
`subjobtypelevelname` string, 
`welfaretaglist` string, 
`cityid` int, 
`workcity` string, 
`worktypeCode` int, 
`worktype` string, 
`workingexpCode` int, 
`workingexp` string, 
`companyid` string, 
`companynumber` string, 
`companyscaletypetagsnew` string, 
`companyname` string, 
`rootcompanynumber` string, 
`companylogo` string, 
`companysize` string, 
`companyurl` string)
PARTITIONED BY (partition_date string);
CREATE TABLE `dwd_jobfree`.`dwd_jobfree_db_jobfree_t_resume` (
   `id` string,
  `eduHighestLevel` int,
  `eduHighestLevelTranslation` string,
  `workingexpCode` int,
  `workingexp` string,
  `worktypeCode` int,
  `worktype` string,
  `workcity` int,
  `workcityTranslation` string,
  `workcity2` int,
  `workcity2Translation` string,
  `workcity3` int,
  `workcity3Translation` string,
  `subjobtypelevel` bigint,
  `subjobtypelevelname` string,
  `skilllabel` string,
  `propertycode` int,
  `property` string,
  `preferredSalaryMin` int,
  `preferredSalaryMax` int,
  `SelfEvaluate` string,
  `created_time` timestamp,
  `last_update` timestamp,
  `user_id` int,
  `cdc_sync_date` timestamp
) PARTITIONED BY (partition_date string);
CREATE TABLE `dwd_jobfree.dwd_jobfree_db_spider_t_company`(	
  `companyid` string, 	
  `rootcompanynumber` string, 	
  `companynumber` string, 	
  `companyscaletypetagsnew` string, 	
  `companyname` string, 	
  `companylogo` string,
  `industryCompanyTags` string,
  `industryName` 	string,
  `companysize` string, 	
  `companyurl` string, 	
  `job_num` bigint
  )	PARTITIONED BY (partition_date string);
  create TABLE `dwd_jobfree`.`dwd_jobfree_db_jobfree_t_resume_train`(
  `user_id` int,
  `eduHighestLevel` int,
  `workingexpCode` int,
  `worktypeCode` int,
  `workcity` int,
  `subjobtypelevel` bigint,
  `propertycode` int,
  `preferredSalaryMin` int,
  `preferredSalaryMax` int,
  `SelfEvaluate` string,
  `skilllabel` string
);
create TABLE `dwd_jobfree`.`dwd_jobfree_db_spider_t_jobs_train`(
  `job_id` int,
  `educationCode` int,
  `workingexpCode` int,
  `worktypeCode` int,
  `workcity` int,
  `subjobtypelevel` bigint,
  `propertycode` int,
  `salary_min` int,
  `salary_max` int,
  `jobsummary` string, 
  `skilllabel` string
);
create TABLE `ads_jobfree`.`ads_jobfree_db_jobfree_t_recommendforallusers`(
  `user_id` int,
  `recommendations` string
);
create TABLE `ads_jobfree`.`ads_jobfree_db_jobfree_t_hotjobs_TOP20`(
  `job_id` int,
  `weight` bigint
)PARTITIONED BY (partition_date string);