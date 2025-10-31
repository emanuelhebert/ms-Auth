import base64
import hashlib

def generate_token(email: str, document: str):
    raw = f"{email}:{document}"
    token_bytes = base64.b64encode(raw.encode("utf-8"))
    return token_bytes.decode("utf-8")

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, hashed: str):
    return hash_password(password) == hashed
