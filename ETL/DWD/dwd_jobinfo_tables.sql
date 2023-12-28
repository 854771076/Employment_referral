
create database dwd_jobfree;
CREATE TABLE `dwd_jobfree`.`dwd_jobfree_db_spider_t_jobs`(
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

CREATE TABLE `dwd_jobfree`.`dwd_jobfree_db_spider_t_company`(	
  `companyid` string, 	
  `rootcompanynumber` string, 	
  `companynumber` string, 	
  `companyscaletypetagsnew` string, 	
  `companyname` string, 	
  `companylogo` string,
  `industryCompanyTags` string,
  `industryName` 	string,
  `propertycode` int,
  `property` string,
  `companysize` string, 	
  `companyurl` string, 	
  `job_num` bigint
  )	PARTITIONED BY (partition_date string);

CREATE TABLE `dwd_jobfree`.`dwd_jobfree_db_jobfree_t_hotjobs`(	
  `job_id` string, 	
  `weight` bigint
  )	PARTITIONED BY (partition_date string);
-- 用户浏览数据加工
select job_id,click_num from
(select *, 
row_number() over (distribute by job_id sort by last_update DESC ) as rank ,
sum(`count`) over (PARTITION by job_id) as click_num
from `ods_jobfree`.`ods_jobfree_db_jobfree_t_clickjobs`) t1
where t1.rank = 1 ;
--用户收藏数据加工，1收藏相当于10点击
select job_id,count(*)*10 as star_num_weight from ods_jobfree.ods_jobfree_db_jobfree_t_starjobs group by job_id;

-- 处理jobs
select 
job_id,
jobId,
get_json_object(number,"$") as number,
get_json_object(name,"$") as name,
Case when
get_json_object(education,"$")="不限" then -1
when get_json_object(education,"$")="博士" then 8
when get_json_object(education,"$")="MBA/EMBA" then 7
when get_json_object(education,"$")="硕士" then 6
when get_json_object(education,"$")="本科" then 5
when get_json_object(education,"$")="大专" then 4
when get_json_object(education,"$")="高中" then 3
when get_json_object(education,"$")="中专/中技" then 2
when get_json_object(education,"$")="初中及以下" then 1
else -1
end as educationCode,
get_json_object(education,"$") as education,
CONCAT_WS(',',split(regexp_replace( industryCompanyTags, '\\\\[|\\\\]|"', ''),',')) as industryCompanyTags,
get_json_object(industryName,"$") as industryName,
get_json_object(jobSummary,"$") as jobSummary,
get_json_object(positionUrl,"$") as positionUrl,
get_json_object(positionSourceTypeUrl,"$") as positionSourceTypeUrl,
get_json_object(property,"$") as property,
cast (get_json_object(propertyCode,"$") as int) as propertyCode,
get_json_object(recruitNumber,"$") as recruitNumber,
get_json_object(salary60,"$") as salary60,
get_json_object(salaryReal,"$") as salaryReal,
cast (split(get_json_object(salaryReal,"$"),"-")[0] as int) as salary_min,
cast (split(get_json_object(salaryReal,"$"),"-")[1] as int) as salary_max,
get_json_object(salaryType,"$") as salaryType,

get_json_object(salaryCount,"$") as salaryCounte,
CONCAT_WS('/',split(regexp_replace(get_json_object(skillLabel,"$[*].value"), '\\\\[|\\\\]|"', ''),',')) as skillLabel,
cast(get_json_object(publishTime,"$") as timestamp) as publishTime,
get_json_object(cityDistrict,"$") as cityDistrict,
get_json_object(streetId,"$") as streetId,
get_json_object(streetName,"$") as streetName,
cast (get_json_object(subJobTypeLevel,"$") as BIGINT) as subJobTypeLevel,
get_json_object(subJobTypeLevelName,"$") as subJobTypeLevelName,
CONCAT_WS('/',split(regexp_replace(welfareTagList, '\\\\[|\\\\]|"', ''),',')) as welfareTagList,
cast (get_json_object(Cityid,"$") as int) as Cityid,
get_json_object(workCity,"$") as workCity,
Case when
get_json_object(workType,"$")="不限" then -1
when get_json_object(workType,"$")="兼职/临时" then 1
when get_json_object(workType,"$")="全职" then 2
when get_json_object(workType,"$")="实习" then 3
when get_json_object(workType,"$")="校园" then 4
else 0
end as workTypeCode ,
get_json_object(workType,"$") as workType,
Case when
get_json_object(workingExp,"$")="不限" then -1
when get_json_object(workingExp,"$")="无经验" then 0
when get_json_object(workingExp,"$")="1年以下" then 1
when get_json_object(workingExp,"$")="1-3年" then 3
when get_json_object(workingExp,"$")="3-5年" then 5
when get_json_object(workingExp,"$")="5-10年" then 10
when get_json_object(workingExp,"$")="10年以上" then 99
else 0
end as workingExpCode ,
get_json_object(workingExp,"$") as workingExp,
companyId,
get_json_object(companyNumber,"$") as companyNumber,
CONCAT_WS('/',split(regexp_replace(companyScaleTypeTagsNew, '\\\\[|\\\\]|"', ''),',')) as companyScaleTypeTagsNew,
get_json_object(companyName,"$") as companyName,
get_json_object(rootCompanyNumber,"$") as rootCompanyNumber,
get_json_object(companyLogo,"$") as companyLogo,
get_json_object(companySize,"$") as companySize,
get_json_object(companyUrl,"$") as companyUrl
from ods_jobfree.ods_jobfree_db_spider_t_jobs





-- 获取最新简历到dwd
select id, eduhighestlevel, eduhighestleveltranslation, workingexpcode, workingexp, worktypecode, worktype, workcity, workcitytranslation, workcity2, workcity2translation, workcity3, workcity3translation, cast(subjobtypelevel as bigint) as subjobtypelevel, subjobtypelevelname, skilllabel, propertycode, property, preferredsalarymin, preferredsalarymax, selfevaluate, created_time, last_update, user_id, cdc_sync_date
from (select *, row_number() over (distribute by id sort by last_update DESC ) as rank from `ods_jobfree`.`ods_jobfree_db_jobfree_t_resume`) t1
where t1.rank = 1

-- 获取公司数据
SELECT 
companyid,rootcompanynumber,companynumber,companyscaletypetagsnew,companyname,companylogo,industryCompanyTags,industryName,propertycode,property,companysize,companyurl,job_num
from (select *, 
row_number() over (distribute by companynumber sort by publishtime DESC ) as rank ,
count(number) over (PARTITION by companynumber) as job_num
from `dwd_jobfree`.`dwd_jobfree_db_spider_t_jobs`) t1
where t1.rank = 1 order by job_num desc;

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
)
select user_id, 
if(eduhighestlevel is not null,eduhighestlevel,0) as eduhighestlevel, 
if(workingexpCode is not null,workingexpCode,0) as workingexpCode, 
if(worktypeCode is not null,worktypeCode,0) as worktypeCode, 
(if(workcity is not null,workcity,0)+if(workcity2 is not null,workcity2,if(workcity is not null,workcity,0))+if(workcity3  is not null,workcity3,if(workcity  is not null,workcity,0))) as workcity, 
if(subjobtypelevel  is not null,subjobtypelevel,0) as subjobtypelevel, 
if(propertycode  is not null,propertycode,0) as propertycode, 
if(preferredsalarymin  is not null,preferredsalarymin,0) as preferredsalarymin, 
if(preferredsalarymax  is not null,preferredsalarymax,0) as preferredsalarymax,
SelfEvaluate,
skilllabel
from dwd_jobfree.dwd_jobfree_db_jobfree_t_resume


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
)
SELECT job_id,educationcode, workingexpCode, worktypeCode, cityid*3 as cityid, subjobtypelevel, propertycode,salary_min, salary_max,jobsummary,skilllabel FROM dwd_jobfree.dwd_jobfree_db_spider_t_jobs