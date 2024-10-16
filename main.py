from typing import Annotated
from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.responses import RedirectResponse
from jinja2_fragments.fastapi import Jinja2Blocks

app = FastAPI()

templates = Jinja2Blocks(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="home.jinja2", context = {
        "request": request,
    })
