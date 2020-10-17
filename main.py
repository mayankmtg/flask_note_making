from flask import Flask, request
from flask_restful import Api, Resource
from flask_mysqldb import MySQL
from uuid import uuid1
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configure MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mayank'
app.config['MYSQL_PASSWORD'] = 'Mayank@123'
app.config['MYSQL_DB'] = 'flask_example'

mysql = MySQL(app)

def get_user(username):
    cur = mysql.connection.cursor()
    cur.execute("select username, uuid from users where username = '" + username + "';")
    rc = 0
    username = None
    user_id = None
    for row in cur:
        rc+=1
        username = row[0]
        user_id = row[1]
    cur.close()
    if rc == 1:
        return user_id
    return None

def get_user_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("select username, uuid from users where uuid = '" + user_id + "';")
    rc = 0
    username = None
    user_id = None
    for row in cur:
        rc+=1
        username = row[0]
        user_id = row[1]
    cur.close()
    if rc == 1:
        return user_id
    return None

def verify_user(username, password):
    cur = mysql.connection.cursor()
    cur.execute("select uuid from users where username = '" + username + "' and password = '"+ password+"';")
    rc = 0
    user_id = None
    for row in cur:
        rc+=1
        user_id = row[0]
    cur.close()
    if rc == 1:
        return user_id
    return None

def register_user(username, password) -> bool:
    try:
        if get_user(username) != None:
            raise Exception("User with same username exists")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password, uuid) VALUES (%s, %s, %s)", (username, password, str(uuid1())))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception:
        return False
    return False

def list_all_notes(user_id):
    if user_id == None:
        return []
    try:
        cur = mysql.connection.cursor()
        cur.execute("select note from notes where uuid = '" + user_id + "';")
        notes = []
        for row in cur:
            notes.append(row[0])
        cur.close()
        return notes
    except Exception:
        return []

def save_note(note, user_id) -> bool:
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes(note, uuid) VALUES (%s, %s);", (note, user_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception:
        return False
    return False

@app.route("/app/user", methods = ["POST"])
def register():
    if request.method == "POST":
        registration = request.json
        username = registration.get("username")
        password = registration.get("password")
        if register_user(username, password):
            return {"status": "account created"}
        else:
            return {"status": "failure"}
    return {"status": "failure"}

@app.route("/app/user/auth", methods = ["POST"])
def login():
    if request.method == "POST":
        app.logger.info('LOGIN POST')
        credentials = request.json
        username = credentials.get("username")
        password = credentials.get("password")
        user_id = verify_user(username, password)
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
    return {"status": "failure"}

@app.route("/app/sites/list/", methods = ["GET"])
def list_notes():
    if request.method == "GET":
        user_id = request.args.get("user")
        return {"notes": list_all_notes(user_id)}

@app.route("/app/sites", methods = ["POST"])
def save_notes():
    if request.method == "POST":
        user_id = request.args.get("user")
        if user_id == None or get_user_id(user_id) == None:
            return {'status': 'failure'}
        data = request.json
        note_string = data.get('note')
        if note_string == None:
            return {'status': 'failure'}
        if save_note(note_string, user_id):
            return {'status': 'success'}
        else:
            return {'status': 'failure'}
    {'status': 'failure'}

if __name__ == "__main__":
    app.run(debug = False)