
import time
from urllib.request import Request, urlopen
import json 
import mysql.connector as mysql 
import os 
from datetime import datetime 
import ast 
from multiprocessing import Process


from dotenv import load_dotenv
load_dotenv("credentials.env") 


db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def on(): 
    
        print ('shades turned on >>>') # print information on terminal 
        time.sleep(1)

def off():  
     
        print ('shades turned off <<<')
        time.sleep(1)
def dim(): 
        
        print ('shades dimmed vvv')
        time.sleep(1)


def get_data():
   
   db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
   
   # preparing a cursor object
   cursor = db.cursor()


   # query the database with the column names. .execute() executes the given query in the database.
   cursor.execute("SELECT sunday, monday, tuesday, wednesday, thursday, friday, saturday FROM personalized_schedule ORDER BY id DESC LIMIT 1;")
   
   # fetch the remaining rows
   records = cursor.fetchone()


   # disconnecting from server
   db.close()


   response = {'sunday':ast.literal_eval(records[0]), 'monday':ast.literal_eval(records[1]), 'tuesday':ast.literal_eval(records[2]), 'wednesday':ast.literal_eval(records[3]), 'thursday':ast.literal_eval(records[4]), 'friday':ast.literal_eval(records[5]), 'saturday':ast.literal_eval(records[6])}
   
   return response
   

def post_data(): 

    ### READS DATA: JSON  ---> INT LIST ###
    
    url='http://localhost:6543/update_schedule'

    response=urlopen(url) 

    data=json.loads(response.read())  
    
    ### READS DATA: JSON  ---> INT LIST ###
    
    ### PARSES JSON DATA ###  

    data=data['schedule']

    ### PARSES JSON DATA ###

    ### UPDATES SQL TABLE ###

    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    
    cursor=db.cursor() 

    query="INSERT INTO personalized_schedule (sunday, monday, tuesday, wednesday, thursday, friday, saturday) values (%s,%s,%s,%s,%s,%s,%s)" 

    values=[str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]), str(data[6])]

    cursor.execute(query,values)   

    db.commit()  
    db.close()
    ### UPDATES SQL TABLE### 

def posting_process():   
    while True:

        date=datetime.now()

        current_second=date.second

        ##on the 45th minute, check if the schedule has been changed and update accordingly.
        if current_second==55: 
            post_data()

def setting_process(): 
    while True: 
         
         date=datetime.now() 

         current_weekday=date.weekday() #weekday defines days starting with Monday not Sunday 
         current_hour=9
         current_second=date.second


         if current_weekday==0: ## Monday 
              
              response=get_data() 

              data=response['monday']

              state=data[current_hour] 

              if state==0 and current_second==0: ##current minute = 0 to only change on the beginning of the hour.
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()

         elif current_weekday==1: ## Tuesday 
              
              response=get_data() 

              data=response['tuesday'] 

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()
              
         elif current_weekday==2: ## Wednesday  
              
              response=get_data() 

              data=response['wednesday'] 

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()
              
         elif current_weekday==3: ## Thursday 
              
              response=get_data() 

              data=response['thursday']

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()
              
         elif current_weekday==4:  ## Friday 
              
              response=get_data() 

              data=response['friday'] 

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()

         elif current_weekday==5: ## Saturday 
              
              response=get_data() 

              data=response['saturday'] 

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()
         
         elif current_weekday==6: ## Sunday 
              
              response=get_data() 

              data=response['sunday'] 

              state=data[current_hour] 

              if state==0 and current_second==0: 
                   off() 
              elif state==1 and current_second==0: 
                   dim() 
              elif state==2 and current_second==0: 
                   on()
     

     



if __name__ == '__main__': # Program entrance 
    
 
    p=Process(target=posting_process) 
    p.start() 
    setting_process()
    
