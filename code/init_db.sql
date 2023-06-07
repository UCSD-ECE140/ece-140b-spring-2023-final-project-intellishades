create database if not exists intellishades;

use intellishades;

-- Remove everything to reset for testing
drop table if exists users;
drop table if exists user_sessions;
drop table if exists device;
drop table if exists schedule;

create table if not exists users (
  id         integer auto_increment primary key,
  first_name varchar(64) not null,
  last_name  varchar(64) not null,
  email  varchar(64) not null,
  username   varchar(64) not null unique,
  password_hash   varchar(64) not null,
  /* security_hash   varchar(64) not null, */
  created_at timestamp not null default current_timestamp
);

create table if not exists user_sessions (
  id integer auto_increment primary key,
  session_id varchar(64),
  session_data json not null,
  created_at timestamp not null default current_timestamp
);

create table if not exists device (
    id         integer auto_increment primary key,
    user_id integer not null,
    device_info json not null,
    created_at timestamp not null default current_timestamp
);

create table if not exists schedule (
    id         integer auto_increment primary key,
    schedule_info json not null,
    created_at timestamp not null default current_timestamp
);