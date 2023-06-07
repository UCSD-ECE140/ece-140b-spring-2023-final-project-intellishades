# Add the necessary imports
import mysql.connector as mysql
import os

# Read Database connection variables  
from dotenv import load_dotenv
load_dotenv("credentials.env") 

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']


# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor() 

cursor.execute("DROP DATABASE if exists intellishades;") 

cursor.execute("create database if not exists intellishades;") 
cursor.execute("use intellishades;")


cursor.execute("drop table if exists users;") 
cursor.execute("drop table if exists user_sessions;")
cursor.execute("drop table if exists device;") 
cursor.execute("drop table if exists schedule;")  


try:
   cursor.execute("""
   create table if not exists users (
  id         integer auto_increment primary key,
  first_name varchar(64) not null,
  last_name  varchar(64) not null,
  email  varchar(64) not null,
  username   varchar(64) not null unique,
  password_hash   varchar(64) not null,
  created_at timestamp not null default current_timestamp
);
      """)  
   

except RuntimeError as err:
   print("runtime error: {0}".format(err)) 
db.commit()
 
try:
   cursor.execute("""
 create table if not exists user_sessions (
  id integer auto_increment primary key,
  session_id varchar(64),
  session_data json not null,
  created_at timestamp not null default current_timestamp
);
      """)  
   

except RuntimeError as err:
   print("runtime error: {0}".format(err)) 
db.commit() 

try:
   cursor.execute("""
create table if not exists device (
    id         integer auto_increment primary key,
    user_id integer not null,
    device_info json not null,
    created_at timestamp not null default current_timestamp
);
      """)  
   

except RuntimeError as err:
   print("runtime error: {0}".format(err)) 
db.commit()  

try:
   cursor.execute("""
create table if not exists schedule (
    id         integer auto_increment primary key,
    schedule_info json not null,
    created_at timestamp not null default current_timestamp
);
      """)  
   

except RuntimeError as err:
   print("runtime error: {0}".format(err)) 
db.commit() 