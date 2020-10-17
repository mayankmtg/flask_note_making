from crypto import encrypt, decrypt

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
        for i in range(len(notes)):
            notes[i] = decrypt(notes[i])
        return notes
    except Exception:
        return []

def save_note(mysql, note, user_id) -> bool:
    try:
        cur = mysql.connection.cursor()
        encrypted_note = encrypt(note)
        cur.execute("INSERT INTO notes(note, uuid) VALUES (%s, %s);", (encrypted_note, user_id))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception:
        return False
    return False