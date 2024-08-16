from flask import Flask, render_template, request, redirect, make_response, url_for
import base64
import json

app = Flask(__name__)

# Dummy user data for authentication
users = {
    "user91019": {"password": "support", "role": "user"},
    "elgat0": {"password": "3lmatador3", "role": "admin"}
}

# Constant key for the single cookie
COOKIE_KEY = 'session'

@app.route('/')
def index():
    # Access the cookie using a constant key
    cookie_data = request.cookies.get(COOKIE_KEY)

    if not cookie_data:
        return redirect(url_for('login'))

    try:
        # Decode cookie data from Base64
        json_data = base64.b64decode(cookie_data.encode()).decode()
        data = json.loads(json_data)
        role = data.get('role')

        # Handle different roles
        if role == 'admin':
            return render_template('admin.html')
        elif role == 'user':
            return render_template('home.html')
    except Exception:
        pass  # Ignore any invalid cookies

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
            # Encode data to Base64
            json_data = json.dumps(data)
            encoded_data = base64.b64encode(json_data.encode()).decode()
            response = make_response(redirect(url_for('index')))
            # Set cookie with a constant key
            response.set_cookie(COOKIE_KEY, encoded_data)
            return response
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie(COOKIE_KEY)  # Delete the single cookie
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")
