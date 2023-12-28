create database ads_jobfree;
create TABLE `ads_jobfree`.`ads_jobfree_db_jobfree_t_recommendforallusers`(
  `user_id` int,
  `recommendations` string
)
create TABLE `ads_jobfree`.`ads_jobfree_db_jobfree_t_hotjobs_TOP20`(
  `job_id` int,
  `weight` bigint
)PARTITIONED BY (partition_date string);
select CAST(job_id as int) as job_id,sum(weight) as weight from dwd_jobfree.dwd_jobfree_db_jobfree_t_hotjobs group by job_id order by weight desc limit 20