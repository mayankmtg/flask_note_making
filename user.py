from uuid import uuid1

def validate_user_input(user_data_json):
    username = user_data_json.get("username")
    password = user_data_json.get("password")
    if username == None or password == None:
        return False
    return True

def get_user(mysql, username):
    cur = mysql.connection.cursor()
    cur.execute("select uuid from users where username = '" + username + "';")
    rc = 0
    user_id = None
    for row in cur:
        rc+=1
        user_id = row[0]
    cur.close()
    if rc == 1:
        return user_id
    return None

def get_user_id(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute("select uuid from users where uuid = '" + user_id + "';")
    rc = 0
    user_id = None
    for row in cur:
        rc+=1
        user_id = row[0]
    cur.close()
    if rc == 1:
        return user_id
    return None

def verify_user(mysql, username, password):
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

def register_user(mysql, username, password) -> bool:
    try:
        if get_user(mysql, username) != None:
            raise Exception("User with same username exists")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password, uuid) VALUES (%s, %s, %s)", (username, password, str(uuid1())))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception:
        return False
    return False
