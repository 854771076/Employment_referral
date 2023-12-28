# compose/mysql/init/init.sql
Alter user 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'fiang123';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
