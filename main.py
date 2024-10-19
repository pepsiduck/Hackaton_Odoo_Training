from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from jinja2_fragments.fastapi import Jinja2Blocks
import sqlite3
import hashlib

crypt = hashlib.new('sha256')

app = FastAPI()

templates = Jinja2Blocks(directory="templates")

db_connection = sqlite3.connect("USERS")

cur = db_connection.cursor()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="home.jinja2", context = {
        "request": request,
    })

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(name="login.jinja2", context = {
        "request": request,
    })

@app.post("/login")
async def post_login(request: Request, response:Response, username:Annotated[str, Form()], password:Annotated[str, Form()]):
    if(username == '' or password == ''):
        return templates.TemplateResponse(name="login.jinja2", context = {
            "request": request,
            "login_error" : "Please complete the from"
        })

    cur.execute("""SELECT password FROM user_info WHERE username = (:username);""", {'username' : username})
    rows = cur.fetchone()

    if(rows == None):
        return templates.TemplateResponse(name="login.jinja2", context = {
            "request": request,
            "login_error" : "Account does not exists"
        })
    
    crypt.update(password.encode())
    if(rows[0] != crypt.hexdigest()):
        return templates.TemplateResponse(name="login.jinja2", context = {
            "request": request,
            "login_error" : "Password is not correct"
        })
    

    return templates.TemplateResponse(name="login.jinja2", context = {
        "request": request,
        "login_error" : "Logined"
    })

@app.post("/signup")
async def post_login(request: Request, response:Response, username:Annotated[str, Form()], password:Annotated[str, Form()], password_again:Annotated[str, Form()]):

    if(username == '' or password == '' or password_again == ''):
        return templates.TemplateResponse(name="login.jinja2", context={
            "request": request,
            "creation_error": "Please complete the form"
        })

    if(password != password_again):
        return templates.TemplateResponse(name="login.jinja2", context={
            "request": request,
            "creation_error": "The two passwords differ"
        })

    cur.execute("""SELECT username FROM user_info WHERE username = (:username);""", {'username' : username})
    rows = cur.fetchone()

    if(rows != None):
        return templates.TemplateResponse(name="login.jinja2", context={
            "request": request,
            "creation_error": "Account already created"
        })

    crypt.update(password.encode())

    cur.execute("""INSERT INTO user_info (username, password) VALUES ((:username), (:password));""",{'username' : username, 'password' : crypt.hexdigest()})
    db_connection.commit()
    
    return templates.TemplateResponse(name="login.jinja2", context={
            "request": request,
            "message": "Account successfully created"
        })

    
