''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import bcrypt
import json                                       # Used for putting contents to db in the form of json

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('./credentials.env')                 # Read in the environment variables for MySQL
db_config = {
  "host": os.environ['MYSQL_HOST'],
  "user": os.environ['MYSQL_USER'],
  "password": os.environ['MYSQL_PASSWORD'],
  "database": os.environ['MYSQL_DATABASE']
}
session_config = {
  'session_key': os.environ['SESSION_KEY']
}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations on users
# CREATE SQL query
def create_user(first_name:str, last_name:str, email:str, username:str, password:str) -> int:
  # hash Password
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "insert into users (first_name, last_name, email, username, password_hash) values (%s, %s, %s, %s, %s)"
  values = (first_name, last_name, email, username, password)
  try:
    cursor.execute(query, values)
    db.commit()
    db.close()
  except RuntimeError as err:
    return -1
  return cursor.lastrowid

# SELECT SQL query
def select_users(username:str=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if username == None:
    query = f"select id, first_name, last_name, email, username from users"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = 'select first_name, last_name, email, username from users where username=%s'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
  db.close()
  return result

# Find the id of the user
def get_user_id(username:str) -> int:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if username == None:
    return -1
  else:
    query = 'select id from users where username=%s'
    cursor.execute(query, (username,))
    result = cursor.fetchone()
  db.close()
  if result:
    return int(result[0])
  else:
    return -1

# UPDATE SQL query
def update_user(old_user_name:str, first_name:str, last_name:str, email:str, username:str, password:str) -> bool:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update users set first_name=%s, last_name=%s, email=%s, username=%s, password_hash=%s where username=%s"
  values = (first_name, last_name, email, username, password, old_user_name)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_user(user_name:str) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'delete from users where username=%s'
  cursor.execute(query, (user_name,))
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users
def check_user_password(username:str, password:str) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'select password_hash from users where username=%s'
  cursor.execute(query, (username,))
  result = cursor.fetchone()
  cursor.close()
  db.close()
  if result is not None:
    return bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))
  return False

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations on comments
# CREATE SQL query
def create_comment(section_id:int, team_id:int, user_id: int, content:dict) -> int:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  try:
    query = "insert into comments (section_id, team_id, user_id, content) values (%s, %s, %s, %s)"
    values = (section_id, team_id, user_id, json.dumps(content))
    cursor.execute(query, values)
    db.commit()
    result = cursor.lastrowid
    db.close()
    return result
  except RuntimeError as err:
    return -1

# SELECT SQL query
def select_user_comments(user_id:int=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if user_id == None:
    query = f"select comments.section_id, comments.team_id, users.username, comments.content from comments FULL OUTER JOIN users ON comments.user_id = users.id"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select comments.section_id, comments.team_id, users.username, comments.content from comments FULL OUTER JOIN users ON comments.user_id = users.id where comments.user_id={user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
  db.close()
  return result

# SELECT SQL query
def select_team_comments(section_id:int=None, team_id:int=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if section_id == None:
    query = f"select comments.id, comments.section_id, comments.team_id, users.username, comments.content from comments INNER JOIN users ON comments.user_id = users.id"
    cursor.execute(query)
    result = cursor.fetchall()
  elif team_id==None:
    query = f"select comments.id, comments.section_id, comments.team_id, users.username, comments.content from comments INNER JOIN users ON comments.user_id = users.id where comments.section_id={section_id}"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select comments.id, comments.section_id, comments.team_id, users.username, comments.content from comments INNER JOIN users ON comments.user_id = users.id where comments.section_id={section_id} AND comments.team_id={team_id}"
    cursor.execute(query)
    result = cursor.fetchall()
  db.close()
  return result

# UPDATE SQL query
def update_comment(comment_id:int, section_id:int, team_id:int, user_id: int, content:dict) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update comments set content=%s where section_id=%s AND team_id=%s AND user_id=%s AND id=%s"
  values = (json.dumps(content), section_id, team_id, user_id, comment_id)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# DELETE SQL query
def delete_comment(comment_id:int, section_id:int, team_id:int, user_id: int) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  cursor.execute(f"delete from comments where section_id={section_id} AND team_id={team_id} AND user_id={user_id} AND id={comment_id}")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False



# get schedule data
def get_schedule_data():
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  
  # access mysql data 
  cursor.execute(f"SELECT COUNT(*) AS total_count FROM schedule;")
  schedule_count = cursor.fetchone()
  schedule_info = []
  if(schedule_count[0] == 0):
    # return json that is all black 
    all_black = [[0] * 24 for _ in range(7)]  
    schedule_info = all_black # json.dumps(all_black)
  else:
    # return saved data
    cursor.execute(f"SELECT schedule_info FROM schedule ORDER BY created_at DESC LIMIT 1;")
    schedule_info = cursor.fetchone()[0]
    
  db.close()
  return schedule_info


def update_schedule_data(schedule_data):
  db = mysql.connect(**db_config)
  cursor = db.cursor()  
  query = "INSERT INTO schedule (schedule_info) values (%s)"
  values = ([json.dumps(schedule_data)])
  cursor.execute(query, values)
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False