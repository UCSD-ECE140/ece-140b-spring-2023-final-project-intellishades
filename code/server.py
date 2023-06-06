''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
# The main FastAPI import and Request/Response objects
from sessiondb import Sessions
from fastapi import FastAPI, Request, Response
# Used to redirect to another route
from fastapi.responses import RedirectResponse
# Used to define the model matching the DB Schema
from pydantic import BaseModel
# Used for returning HTML responses (JSON is default)
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
# Used for generating HTML from templatized files
from fastapi.templating import Jinja2Templates
# Used for making static resources available to server
from fastapi.staticfiles import StaticFiles
# Additional imports for forms
from fastapi import Request, Form
# Used for running the app directly through Python
import uvicorn
# Import helper module of database functions!
import dbutils as db
import json
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import numpy as np                                # Used for transposing arrays of schedule info
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
# Specify the "app" that will run the routing
app = FastAPI()
# Specify where the HTML files are located
views = Jinja2Templates(directory='views')
# Specify where the static files are located
static_files = StaticFiles(directory='public')
# Mount the static files directory to /public
app.mount('/public', static_files, name='public')

# Use MySQL for storing session data
sessions = Sessions(
    db.db_config, secret_key=db.session_config['session_key'], expiry=60000)

# Use in-memory dictionary to store session data – CAUTION: all sessions are deleted upon server restart
# from sessiondict import Sessions
# sessions = Sessions(secret_key=db.session_config['session_key'], expiry=600)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define a User class that matches the SQL schema we defined for our users


class User(BaseModel):
    fname: str
    lname: str
    email: str
    uname: str
    pword: str


class Visitor(BaseModel):
    username: str
    password: str


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# A function to authenticate users when trying to login or use protected routes


def authenticate_user(username: str, password: str) -> bool:
    return db.check_user_password(username, password)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Authentication routes (login, logout, and a protected route for testing)


@app.get('/login')
async def get_login(request: Request) -> HTMLResponse:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        return RedirectResponse(url="/dashboard", status_code=302)
    else:  # Go to profile page if the user already logged in
        with open("login.html") as html:
            return HTMLResponse(content=html.read())


@app.post('/login')
async def post_login(visitor: Visitor, request: Request, response: Response) -> dict:
    username = visitor.username
    password = visitor.password

    # Invalidate previous session if logged in
    session = sessions.get_session(request)
    if len(session) > 0:
        sessions.end_session(request, response)

    # Authenticate the user
    if authenticate_user(username, password):
        session_data = {'username': username, 'logged_in': True}
        session_id = sessions.create_session(response, session_data)
        return {'message': 'Login successful', 'session_id': session_id}
    else:
        return {'message': 'Invalid username or password', 'session_id': 0}


@app.get('/logout', response_class=HTMLResponse)
async def post_logout(request: Request, response: Response) -> HTMLResponse:
    sessions.end_session(request, response)
    return RedirectResponse(url="/login")

# User is registering a new account


@app.post('/register')
async def register_account(user: User, request: Request, response: Response) -> dict:
    firstName = user.fname
    lastName = user.lname
    username = user.uname
    uEmail = user.email
    password = user.pword

    result = db.create_user(firstName, lastName, uEmail, username, password)
    # Do not log in if user creation failed
    if result == -1:
        return {'message': 'Invalid user information', 'session_id': 0}

    # Now log the user in and go to dashboard
    # Authenticate the user
    if authenticate_user(username, password):
        session_data = {'username': username, 'logged_in': True}
        session_id = sessions.create_session(response, session_data)
        return {'message': 'Login successful', 'session_id': session_id}
    else:
        return {'message': 'Invalid username or password', 'session_id': 0}

# User is modifying information of their current account


@app.put('/updateuser')
async def update_account(user: User, request: Request, response: Response) -> dict:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        firstName = user.fname
        lastName = user.lname
        username = user.uname
        uEmail = user.email
        password = user.pword
        old_user_name = session.get('username')
        # Log user out when they modify the information
        sessions.end_session(request, response)
        result = db.update_user(old_user_name, firstName,
                                lastName, uEmail, username, password)
        if result == False:
            return {'message': 'Invalid user information', 'session_id': 0}
        else:
            return {'message': 'Modification succeeded', 'session_id': -1}
    else:
        return {'message': 'Invalid user information', 'session_id': 0}

# User is modifying information of their current account


@app.put('/resetuser')
async def reset_password(user: User, request: Request, response: Response) -> dict:
    firstName = user.fname
    lastName = user.lname
    username = user.uname
    uEmail = user.email
    password = user.pword
    existingInfo = db.select_users(username)
    if (existingInfo != None and firstName == existingInfo[0] and lastName == existingInfo[1]
            and uEmail == existingInfo[2] and username == existingInfo[3]):
        result = db.update_user(username, firstName,
                                lastName, uEmail, username, password)
        return {'message': 'Password Reset succeeded', 'session_id': 0}
    else:
        return {'message': 'Invalid user information', 'session_id': -1}

# User is modifying information of their current account


@app.delete('/deleteuser')
async def delete_account(request: Request, response: Response) -> dict:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        old_user_name = session.get('username')
        # Log user out when they modify the information
        sessions.end_session(request, response)
        result = db.delete_user(old_user_name)
        if result == False:
            return {'message': 'Invalid user deletion', 'session_id': 0}
        else:
            return {'message': 'Deletion succeeded', 'session_id': -1}
    else:
        return {'message': 'Invalid user information', 'session_id': 0}


@app.get('/register')
async def go_register() -> HTMLResponse:
    with open("register.html") as html:
        return HTMLResponse(content=html.read())


@app.get('/reset')
async def go_register() -> HTMLResponse:
    with open("reset.html") as html:
        return HTMLResponse(content=html.read())

# Open profile when the user is authenticated


@app.get('/dashboard', response_class=HTMLResponse)
async def open_user_profile(request: Request) -> HTMLResponse:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        with open("profile.html") as html:
            return HTMLResponse(content=html.read())
    else:  # Redirect user ot log in if there are no valid sessions
        return RedirectResponse(url="/login", status_code=302)

# Open profile when the user is authenticated


@app.get('/userinfo', response_class=JSONResponse)
async def get_userInfo(request: Request) -> dict:
    session = sessions.get_session(request)
    userInfo = {}
    if len(session) > 0 and session.get('logged_in'):
        userInfo = db.select_users(str(session['username']))
    return JSONResponse(userInfo)

# Route to test if user has logged in


@app.get('/protected')
async def get_protected(request: Request) -> dict:
    session = sessions.get_session(request)
    if len(session) > 0 and session.get('logged_in'):
        return {'message': 'Access granted'}
    else:
        return {'message': 'Access denied'}

# GET /sessions to test session maintain and expire


@app.get('/sessions')
async def get_sessions(request: Request) -> dict:
    return sessions.get_session(request)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Index route to load the main page in a templatized fashion
# GET /


@app.get('/', response_class=HTMLResponse)
def get_index() -> HTMLResponse:
    with open("index.html") as html:
        return HTMLResponse(content=html.read())

# Open Schedule page
# GET /schedule


@app.get('/schedule', response_class=HTMLResponse)
def get_schedule() -> HTMLResponse:
    with open("schedule.html") as html:
        return HTMLResponse(content=html.read())


# GET /schedule_data
@app.get('/schedule_data', response_class=JSONResponse)
def get_schedule() -> JSONResponse:
  database_data = db.get_schedule_data()
  stored_data = database_data['schedule']
  # stored_data = eval(stored_data)
  # Must convert to a List before converting into numpy array
  stored_data = np.asarray(stored_data, dtype=int)
  # Apply transpose after converting to numpy array
  stored_data = np.transpose(stored_data)
  # Convert back to a list to return
  stored_data = np.ndarray.tolist(stored_data)
  data_to_send = {
    'device_id': database_data["device_id"],
    'user_id': database_data["user_id"],
    'schedule': stored_data
  }
  print("schedule info in server.py: ", data_to_send)
  return data_to_send

# POST /schedule_data
@app.post('/update_schedule', response_class=JSONResponse)
def update_schedule(data: dict) -> JSONResponse:
  schedule_to_save = np.transpose(data["schedule"])
  data_to_save = {
        'device_id': data["device_id"],
        'user_id': data["user_id"],
        'schedule': np.ndarray.tolist(schedule_to_save)
  }
  db.update_schedule_data(data_to_save)
  # update on pi
#   pi={'device_id': 999,
#  'user_id': 000,
#  'schedule': int(data)}
  
#   return JSONResponse(pi) 
   

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)