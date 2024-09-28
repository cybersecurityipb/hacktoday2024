#!/usr/bin/env python3
import os
import re
import subprocess
from flask import Flask, render_template, request

MAX_FILE_SIZE = 3*1024 # 3 kb limit
SCANNER = './stegoscan'
UPLOAD_DIR = 'uploads/'

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/stegoscan', methods=['POST'])
def stegoscan():
  file = request.files['file']
  # sanitize filename
  filename = re.sub(r'[^a-zA-Z0-9_.-]', '', file.filename)
  file_path = os.path.join(UPLOAD_DIR, filename)
  if request.content_length > MAX_FILE_SIZE:
    return 'File exceeds max size'
  file.save(file_path)
  try:
    output = subprocess.run([SCANNER, file_path], capture_output=True, text=True, timeout=1).stdout
  except subprocess.CalledProcessError as e:
    print(e)
    output = e
  return output

@app.route('/results', methods=['GET'])
def results():
  return render_template('results.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1337)
