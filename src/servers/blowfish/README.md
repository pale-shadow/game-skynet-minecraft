# Blowfish: Neural-Data Vault (MariaDB)

This node hosts the centralized MariaDB instance for the Skynet cluster, serving as the "Neural-Data Vault" for LuckPerms, BlueMap, and other stateful services.

## 1. Security & Credential Management

**CRITICAL:** Never store passwords in cleartext within documentation or scripts. Use the centralized `.envrc` management system as described in `GEMINI.md`.

## 2. Database Initialization

Run these commands inside the MariaDB monitor on `blowfish` (`10.10.12.15`):

```sql
-- 1. Create the database
CREATE DATABASE IF NOT EXISTS bluemap;

-- 2. Create the user and grant access (Replace 'your_password_here')
-- Note: Credentials should be retrieved from the secured .envrc environment.
CREATE USER 'bluemap'@'10.10.8.60' IDENTIFIED BY 'your_password_here';

-- 3. Grant privileges
GRANT ALL PRIVILEGES ON bluemap.* TO 'bluemap'@'10.10.8.60';

-- 4. Apply changes
FLUSH PRIVILEGES;
```

## 3. Verification

Verify the user configuration using the MariaDB monitor:

```sql
SELECT User, Host FROM mysql.user WHERE User = 'bluemap';
```

**Expected Output:**

```text
+-------------+------------+
| User        | Host       |
+-------------+------------+
| bluemap     | 10.10.8.60 |
+-------------+------------+
```

## 4. Hardware Profile
- **Compute:** OpenBSD 7.8 (Host: `blowfish`)
- **Service:** MariaDB Instance
- **Network ID:** Hub-07 (Neural-Data Vault)

---
*Created for theDevilsVoice | Last Updated: April 14, 2026*
