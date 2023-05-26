from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi import Request
from pydantic import BaseModel
from urllib.request import Request, urlopen
import json
import mysql.connector as mysql 
from dotenv import load_dotenv 
import os

import hashlib

app = FastAPI()


# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public") 

@app.get("/test_page", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("test.html") as html:
        return HTMLResponse(content=html.read())

@app.post ("/update_schedule")
def update_schedule(theFields:dict):  
    return JSONResponse(theFields) 


@app.get ("/update_schedule",response_class=JSONResponse)
def update_schedule() -> JSONResponse:  
    data={'device_id': 999,
 'user_id': 000,
 'schedule': [[0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0]]
        }

    return JSONResponse(data) 

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)