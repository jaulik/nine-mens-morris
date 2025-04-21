
# src

## game

## db


# SQL

## /sqlite - SQLite Runtime
The sql/sqlite directory contains two SQLite scripts. These scripts serve to setup or clean **SQLite database**.

 - `sqlite/create_schema.sql`		- creates tables (players, games, statistics) and tiggers
 - `sqlite/drop_db.sql`			- development helper to drop all tables

## /oracle - school project only (Oracle SQL)

The sql/oracle directory contains a complete set of Oracle SQL scripts prepared for the Database Systems course project.
These scripts are not part of the runtime application, they are provided for demonstration of Oracle/PL‑SQL skills.

 - `oracle/create_tables.sql`		- creates tables, seqences and defines referential intengrity constraints
 - `oracle/insert_data.sql`		- inserts sample data into tables
 - `oracle/triggers_update.sql`		- two triggers, procedure, cursor, recalculates statistics table
 - `oracle/select.sql`			- several select statements

