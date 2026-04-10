1. Create the Database and User
Run these commands inside your MariaDB monitor on blowfish:

SQL

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS bluemap;

-- 2. Create the user and allow connections from your Minecraft server IP
CREATE USER 'bluemap'@'10.10.8.60' IDENTIFIED BY 'your_password_here'; -- IMPORTANT: Replace 'your_password_here' with a strong, unique password. Refer to .envrc guidelines for secure credential management.

-- 3. Give the user full access to the bluemap database
GRANT ALL PRIVILEGES ON bluemap.* TO 'bluemap'@'10.10.8.60';

-- 4. Apply changes
FLUSH PRIVILEGES;
2. Verify the Creation
Run your select query again to make sure it's there:

SQL

SELECT User, Host FROM mysql.user WHERE User = 'bluemap';


MariaDB [minecraft]> SELECT User, Host FROM mysql.user;
+-------------+------------+
| User        | Host       |
+-------------+------------+
| PUBLIC      |            |
| betty       | 10.10.8.60 |
| bluemap     | 10.10.8.60 |
| luckperms   | 10.10.8.60 |
| minecraft   | 10.10.8.60 |
| _mysql      | localhost  |
| mariadb.sys | localhost  |
| root        | localhost  |
+-------------+------------+
8 rows in set (0.001 sec)

