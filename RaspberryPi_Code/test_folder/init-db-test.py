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

cursor.execute("DROP DATABASE if exists Schedule;") 

cursor.execute("CREATE DATABASE if not exists Schedule;")
cursor.execute("USE Schedule;") 

cursor.execute("drop table if exists personalized_schedule;") 


try:
   cursor.execute("""
   CREATE TABLE personalized_schedule (
       id            integer  AUTO_INCREMENT PRIMARY KEY,
       sunday        VARCHAR(100) NOT NULL, 
       monday        VARCHAR(100) NOT NULL,
       tuesday       VARCHAR(100) NOT NULL,
       wednesday     VARCHAR(100) NOT NULL, 
       thursday      VARCHAR(100) NOT NULL, 
       friday        VARCHAR(100) NOT NULL,
       saturday      VARCHAR(100) NOT NULL
      );
      """)  
   
   
   #TESTING DUMMY INPUT

   query="INSERT INTO personalized_schedule (sunday, monday, tuesday, wednesday, thursday, friday, saturday) values (%s,%s,%s,%s,%s,%s,%s)"  
   values=('[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]')
   cursor.execute(query,values) 
   

except RuntimeError as err:
   print("runtime error: {0}".format(err)) 
db.commit()
 
