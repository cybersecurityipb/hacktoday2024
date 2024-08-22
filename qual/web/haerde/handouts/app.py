from flask import *
from psycopg2 import *
from werkzeug.utils import secure_filename
from functools import wraps
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

conn = connect(dbname=os.getenv('DBNAME'), user=os.getenv('DBUSER'), password=os.getenv('DBPASS'), host=os.getenv('DBHOST'), port=os.getenv('DBPORT'))
cur = conn.cursor()

def create_tables():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS accepted_users (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            filename VARCHAR(255) NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cur.execute('''
        INSERT INTO users (username, password) 
        VALUES (%s, %s) 
        ON CONFLICT (username) DO NOTHING
    ''', ("admin", os.getenv('ADMINPASS')))
    cur.execute('''
        INSERT INTO accepted_users (user_id) 
        SELECT id FROM users WHERE username = 'admin' 
        ON CONFLICT DO NOTHING
    ''')
    conn.commit()

create_tables()

def visit(target_url):
    options = Options()
    options.headless = True
    service = Service(executable_path='/usr/local/bin/geckodriver') 
    os.environ['MOZ_HEADLESS'] = '1'

    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(15)

        driver.get('http://127.0.0.1:5000/login')

        USERNAME = 'admin'
        PASSWORD = os.getenv('ADMINPASS', 'password_admin_lah_boy')

        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        submit_button.click()
        sleep(1)

        driver.get(target_url)

    except TimeoutException:
        print(f"Error: Loading {target_url} took too long.")
        return False
    except WebDriverException as e:
        print(f"Error: WebDriverException occurred: {e}")
        return False
    finally:
        sleep(3)
        driver.quit()

    return True

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def accepted_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cur.execute("SELECT * FROM accepted_users WHERE user_id = %s", (session['user_id'],))
        accepted_user = cur.fetchone()
        if not accepted_user:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] != 'admin':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    cur.execute("SELECT * FROM history WHERE username = %s", (session.get('username'),))
    return render_template('index.html', data=cur.fetchall())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur.execute("SELECT id, username FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        if user:
            if user[1] == 'admin' and request.remote_addr != '127.0.0.1':
                abort(403)
            session['user_id'] = user[0]
            session['username'] = user[1]
            if user[1] == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/sendcv', methods=['GET', 'POST'])
@login_required
@accepted_required
def send_cv():
    if request.method == 'POST':
        username = session['username']
        file = request.files['cv']
        
        if file and allowed_file(file.filename):

            if file.content_length > app.config['MAX_CONTENT_LENGTH']:
                flash('File exceeds maximum allowed size of 2 MB', 'danger')
                abort(400)
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            cur.execute("INSERT INTO history (username, filename) VALUES ('%s', '%s')" % (username, filename))
            conn.commit()

            flash('File successfully uploaded', 'success')
            return redirect(url_for('send_cv'))
        else:
            flash('Invalid file type or no file selected', 'danger')
            abort(400)

    return render_template('sendcv.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    if request.method == 'POST':
        username = request.form['username']
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            cur.execute("INSERT INTO accepted_users (user_id) VALUES (%s)", (user[0],))
            conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html')

@app.route('/report', methods=['POST'])
def report():
    url = request.form['url']
    if not (url.startswith('http://') or url.startswith('https://')):
        abort(400)

    success = visit(url)
    if success:
        return "URL visited", 200
    else:
        return "Failed to visit URL", 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')