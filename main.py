from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from jinja2_fragments.fastapi import Jinja2Blocks
import sqlite3

app = FastAPI()

templates = Jinja2Blocks(directory="templates")

db_connection = sqlite3.connect("users.db")

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
