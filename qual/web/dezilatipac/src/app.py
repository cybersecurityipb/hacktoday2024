# app.py
from flask import Flask, request, jsonify, abort
import os

app = Flask(__name__)

def validate_command(command):
    allowed_commands = ['whoami']
    command_parts = command.split()
    if not command_parts:
        abort(400, description="Invalid command")
    command_name = command_parts[0]
    if any(name in allowed_commands for name in allowed_commands if command_name.endswith(name)):
        return
    abort(400, description="Invalid command")

@app.before_request
def authenticate():
    token = request.headers.get('Authorization')
    if token != 'ga_harus_login_sih:D':
        abort(401, description="Unauthorized")

@app.route('/execute', methods=['POST'])
def execute():
    command = request.json.get('command', '')
    if not command:
        abort(400, description="No command provided")
    validate_command(command)
    command = command.replace(command[0], command[0].upper())
    result = os.popen(command).read()
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
