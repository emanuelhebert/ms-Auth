import base64
import hashlib
from security.crypto import encrypt_token, decrypt_token

def generate_token(email: str, document: str):
    raw = f"{email}:{document}"
    token_bytes = base64.b64encode(raw.encode("utf-8"))
    return token_bytes.decode("utf-8")

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, hashed: str):
    return hash_password(password) == hashed

def create_access_token(data: dict):
    jwt_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")
    return encrypt_token(jwt_token)

def decode_access_token(token: str):
    decrypted = decrypt_token(token)
    return jwt.decode(decrypted, JWT_SECRET, algorithms=["HS256"])
