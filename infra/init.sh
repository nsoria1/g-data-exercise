#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    drop table if exists jobs;
    drop table if exists departments;
    drop table if exists hired_employees;
    drop table if exists error_log;
	create table if not exists jobs (id int,job varchar(50));
    create table if not exists departments (id int,department varchar(50));
    create table if not exists hired_employees (id int,name varchar(50),datatime varchar(50),department_id int,job_id int);
    create table if not exists error_log ("data" varchar(50),entity varchar(50),msg varchar(50));
EOSQL