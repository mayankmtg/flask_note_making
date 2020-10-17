def list_all_notes(mysql, user_id):
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

def save_note(mysql, note, user_id) -> bool:
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes(note, uuid) VALUES (%s, %s);", (note, user_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception:
        return False
    return False