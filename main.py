from typing import Annotated

import authentification

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

@app.exception_handler(authentification.RequiresLoginException)
async def exception_handler(request: Request, exc: authentification.RequiresLoginException) -> Response:
    return RedirectResponse("/login")

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

    if(rows[0] != hashlib.sha256(password.encode()).hexdigest()):
        return templates.TemplateResponse(name="login.jinja2", context = {
            "request": request,
            "login_error" : "Password is not correct"
        })
    
    ret = templates.TemplateResponse(name="login.jinja2", context = {
        "request": request,
        "login_error" : "Logined"
    })

    ret.set_cookie("username", authentification.to_token(username))

    return ret

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

    password_db = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("""INSERT INTO user_info (username, password) VALUES ((:username), (:password));""",{'username' : username, 'password' : password_db})
    db_connection.commit()
    
    return templates.TemplateResponse(name="login.jinja2", context={
            "request": request,
            "message": "Account successfully created"
        })

@app.get("/menu")
async def login(request: Request):

    username = authentification.get_user(request)

    return templates.TemplateResponse(name="menu.jinja2", context = {
        "request": request,
    })

@app.post("/logout")
async def post_logout(request: Request, response:Response):
    response = RedirectResponse("/home", status_code=303)
    response.delete_cookie("username")
    return response
