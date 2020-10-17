from flask import Flask, request
from flask_restful import Api, Resource
from flask_mysqldb import MySQL
from uuid import uuid1
import logging
from user import *
from note import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configure MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mayank'
app.config['MYSQL_PASSWORD'] = 'Mayank@123'
app.config['MYSQL_DB'] = 'flask_example'

mysql = MySQL(app)

FAILURE_RESPONSE = {"status": "failure"}

@app.route("/app/user", methods = ["POST"])
def register():
    if request.method == "POST":
        registration = request.json
        username = registration.get("username")
        password = registration.get("password")
        if register_user(mysql, username, password):
            return {"status": "account created"}
        else:
            return FAILURE_RESPONSE
    return FAILURE_RESPONSE

@app.route("/app/user/auth", methods = ["POST"])
def login():
    if request.method == "POST":
        app.logger.info('LOGIN POST')
        credentials = request.json
        username = credentials.get("username")
        password = credentials.get("password")
        user_id = verify_user(mysql, username, password)
        if user_id != None:
            return {
                "status" : "success",
                "userId": user_id
            }
        else:
            return {
                "status" : "failure",
                "userId": "none"
            }
    return FAILURE_RESPONSE

@app.route("/app/sites/list/", methods = ["GET"])
def list_notes():
    if request.method == "GET":
        user_id = request.args.get("user")
        return {"notes": list_all_notes(mysql, user_id)}

@app.route("/app/sites", methods = ["POST"])
def save_notes():
    if request.method == "POST":
        user_id = request.args.get("user")
        if user_id == None or get_user_id(mysql, user_id) == None:
            return FAILURE_RESPONSE
        data = request.json
        note_string = data.get('note')
        if note_string == None:
            return FAILURE_RESPONSE
        if save_note(mysql, note_string, user_id):
            return {'status': 'success'}
        else:
            return FAILURE_RESPONSE
    FAILURE_RESPONSE

if __name__ == "__main__":
    app.run(debug = False)