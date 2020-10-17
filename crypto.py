from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def encrypt(message: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt(encrypted_message: str) -> str:
    key = load_key()
    f = Fernet(key)
    encrypted_message = encrypted_message.encode()
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


