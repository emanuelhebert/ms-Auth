from cryptography.fernet import Fernet

SECRET_KEY = b"chave_gerada_com_fernet"  
fernet = Fernet(SECRET_KEY)

def encrypt_token(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_token(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()