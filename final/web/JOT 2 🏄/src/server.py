from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api import api
from db import Database
from utils import Auth

app = FastAPI(title="JOT2SURF", redoc_url=None, docs_url=None)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    database = Database("database.db")
    database._initdb()
    database.close()

@app.exception_handler(404)
def custom_404_handler(request: Request, exc):
    context = {"request": request}
    return templates.TemplateResponse("404.html", context,status_code=404)

@app.get("/", include_in_schema=False)
def get_index(request: Request):
    if not (jwt := request.cookies.get("auth")):
        return RedirectResponse("/login")
    auth = Auth(jwt)
    if not (auth := auth.load()):
        r = RedirectResponse("/login?err=invalidjwt")
        r.delete_cookie("auth", "/")
        return r
    context = {"request": request, "username": auth.get("sub")}
    if auth.get("verified") == "false":
        return templates.TemplateResponse("index.html", context)
    elif auth.get("verified") == "true":
        return templates.TemplateResponse("verified.html", context)
    else:
        return resp("Something went wrong.", 500)

@app.get("/login", include_in_schema=False)
def get_login(request: Request, err: str = ""):
    context = {"request": request}
    if err == "invalidjwt":
        context["errjwt"] = True
        r = templates.TemplateResponse("login.html", context)
        r.delete_cookie("auth", "/")
        return r
    jwt = request.cookies.get("auth")
    auth = Auth(jwt)
    if (auth := auth.load()):
        return RedirectResponse("/")
    return templates.TemplateResponse("login.html", context)

@app.get("/register", include_in_schema=False)
def get_register(request: Request):
    jwt = request.cookies.get("auth")
    auth = Auth(jwt)
    if (auth := auth.load()):
        return RedirectResponse("/")
    context = {"request": request}
    return templates.TemplateResponse("register.html", context)

@app.get("/logout", include_in_schema=False)
def get_logout(request: Request):
    r = RedirectResponse("/login")
    r.delete_cookie("auth", "/")
    return r

@app.get("/docs", include_in_schema=False)
def get_docs(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("docs.html", context)

@app.get("/redoc", include_in_schema=False)
def get_docs(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("docs.html", context)

@app.get("/.well-known/jwks.json", include_in_schema=False)
def get_jwks():
    return FileResponse("jwks.json")

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    return FileResponse("favicon.ico")

app.include_router(api)
