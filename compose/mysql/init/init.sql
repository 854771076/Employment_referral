# compose/mysql/init/init.sql
Alter user 'root'@'%' IDENTIFIED BY 'fiang123';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
CREATE DATABASE `jobfree` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
