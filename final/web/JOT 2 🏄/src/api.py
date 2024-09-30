from fastapi import APIRouter, Request
from fastapi.responses import Response as resp
from typing import Annotated
from db import Database
from schemas import *
from utils import Auth, emoji, weak_password
import json
import subprocess

api = APIRouter(prefix="/api", tags=["api"])

@api.post("/login")
def post_login(request: Request, req : RegUser):
    database = Database("database.db")
    cur = database.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE username = ?;", (req.username,))
        user = cur.fetchone()
        if (not user) or (user[2] != req.password):
            return resp("Invalid username or password.", 403)
        data = {"sub":user[1], "verified":user[3]}
        token = Auth().encode(data, str(request.base_url))
        r = resp("OK")
        r.set_cookie(key="auth", value=token, path="/")
        return r
    except:
        pass
    finally:
        cur.close()
        database.close()
    return resp("Something went wrong.", 500)

@api.post("/register")
def post_register(req: RegUser):
    if any([len(req.password) > 32, len(req.username) > 32]):
        return resp("Username or password is too long!", 403)
    database = Database("database.db")
    data = (req.username, req.password, "false")
    try:
        cur = database.cursor()
        cur.execute("SELECT username FROM users WHERE username = ?", (req.username,))
        if cur.fetchone():
            return resp("Username is already registered.", 403)
        if len(req.password) < 6:
            return resp(f"{emoji()}\nPassword is too short!", 403)
        elif req.username == req.password:
            return resp("Lol. Username == Password.", 403)
        elif req.password.lower().startswith("password") and len(req.password) < 12:
            return resp(f"Lol. Password == \"{req.password}\"", 403)
        elif weak_password(req.password):
            return resp(f"{emoji()}\n\"{req.password}\" shouldn't be used as password!\nIt's unsafe!", 403)
        cur.execute("INSERT INTO users (username, password, verified) VALUES (?, ?, ?);", data)
    except:
        return resp("Something went wrong (?)", 500)
    finally:
        database.commit()
        database.close()
    return resp("OK")

@api.post("/check_ping_result")
def post_ping(request: Request, req: PingCheck):
    jwt = request.cookies.get("auth")
    auth = Auth(jwt)
    if (not (auth := auth.load())) or (auth.get("verified") != "true"):
        return resp("Only verified users can use our service.", 403)
    r = {}
    try:
        command = f"ping -c 3 {req.ip}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10, text=True)
        r = {"success":True, "output":output}
    except subprocess.CalledProcessError as e:
        output = e.output
        r = {"success":False, "output":output}
    finally:
        return resp(json.dumps(r))

@api.get("/verify_user_account__but_this_endpoint_is_still_under_development")
def get_verify(request: Request, username: str = ""):
    if request.client.host != "127.0.0.1":
        return resp("This endpoint cannot be accessed from external IP address. If you are the administrator, please access directly from our server (localhost).", 403)
    if username == "":
        return resp("Bro is using this endpoint but don't know how to use it?", 400)
    database = Database("database.db")
    data = ("true", username)
    try:
        cur = database.cursor()
        cur.execute("UPDATE users SET verified = ? WHERE username = ?", data)
    except:
        return resp("User not found (?)", 404)
    finally:
        database.commit()
        database.close()
    return resp("OK")
