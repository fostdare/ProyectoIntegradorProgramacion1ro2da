from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from app.routes import router

app = FastAPI(title="Trello Clon API - Programación I", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api")

BASE_DIR = "/home/lilium/Escritorio/proyecto programacion"
_jinja_env = Environment(loader=FileSystemLoader(BASE_DIR + "/templates"))


@app.get("/")
def root(request: Request):
    template = _jinja_env.get_template("index.html")
    return HTMLResponse(content=template.render({"request": request}))
