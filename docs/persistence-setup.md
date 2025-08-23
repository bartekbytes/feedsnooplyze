# Persistence Setup

This document outlines all necessary prerequisites that must be met before feedsnooplyze can connect to the configured **Persistence Layer**.

## Oracle

The appropriate Oracle **schema (user)** must be created in the target database.

Example below is for `Oracle 23ai Free Edition`.

1. Log in as SYSDBA

Use `sqlplus` to connect to the Oracle service as SYSDBA user:

```bash
sqlplus sys/your_sys_password@host_name_or_ip:port/oracle_service_name as sysdba
```

Example (local development):

```bash
sqlplus sys/your_sys_password@localhost:1521/FREEPDB1 as sysdba
```

2. Create the `feedsnooplyze` Schema (User)

```sql
-- Create the user (schema) with password
CREATE USER feedsnooplyze IDENTIFIED BY your_password;

-- Grant essential roles to allow login and object creation
GRANT CONNECT, RESOURCE TO feedsnooplyze;

-- Allow unlimited (or consult with your DBA) quota on USERS tablespace (so user can create tables)
ALTER USER feedsnooplyze QUOTA UNLIMITED ON USERS;
```

### Notes

- In Oracle, creating a **user** automatically creates a **schema** with the same name.
- The `CONNECT` role allows login; `RESOURCE` allows creation of tables, views, procedures, etc.
- Without a quota, the user may be unable to create tables depending on your tablespace setup.

### Summary

Once these steps are completed, the `feedsnooplyze` user will be able to:

- Connect to the `FREEPDB1` pluggable database
- Create and manage its own tables and data

You can now point your application or SQLAlchemy connection to:

```
Service:  FREEPDB1
User:     feedsnooplyze
Password: your_password
Host:     localhost
Port:     1521
```
