from flask import Flask, render_template, request, redirect, make_response, url_for
import base64
import json

app = Flask(__name__)

users = {
    "user91019": {"password": "support", "role": "user"},
    "elgat0": {"password": "3lmatador3", "role": "admin"}
}

COOKIE_KEY = 'session'

@app.route('/')
def index():
    cookie_data = request.cookies.get(COOKIE_KEY)

    if not cookie_data:
        return redirect(url_for('login'))

    try:
        json_data = base64.b64decode(cookie_data.encode()).decode()
        data = json.loads(json_data)
        role = data.get('role')

        if role == 'admin':
            return render_template('admin.html')
        elif role == 'user':
            return render_template('home.html')
    except Exception:
        pass

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            data = {
                'username': username,
                'role': user['role']
            }
            json_data = json.dumps(data)
            encoded_data = base64.b64encode(json_data.encode()).decode()
            response = make_response(redirect(url_for('index')))
            response.set_cookie(COOKIE_KEY, encoded_data)
            return response
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie(COOKIE_KEY)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")
