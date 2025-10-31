from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from datetime import datetime, timedelta

login_attempts = {}

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.get("/")
def read_root():
    return {"message": "API de Autenticação funcionando!"}

@router.get("/signup")
def get_signup_info():
    return {
        "message": "Use POST para criar uma conta",
        "example_body": {
            "email": "string",
            "doc_number": "string", 
            "password": "string",
            "username": "string",
            "full_name": "string"
        }
    }

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.doc_number == user.doc_number)
    ).first():
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    new_user = models.User(
        email=user.email,
        doc_number=user.doc_number,
        password=utils.hash_password(user.password),
        username=user.username,
        full_name=user.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token_str = utils.generate_token(new_user.email, new_user.doc_number)
    token = models.Token(id_user=new_user.id, token=token_str)
    db.add(token)
    db.commit()

    return {"token": token_str, "user_id": new_user.id, "message": "Usuário criado com sucesso"}

@router.get("/login")
def get_login_info():
    return {
        "message": "Use POST para fazer login",
        "example_body": {
            "login": "string (email ou username)",
            "password": "string"
        }
    }

@router.post("/login")
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    user_key = payload.login
    if user_key in login_attempts:
        attempts = login_attempts[user_key]
        if attempts["count"] >= 3 and now < attempts["blocked_until"]:
            remaining = (attempts["blocked_until"] - now).seconds // 60
            raise HTTPException(
                status_code=429,
                detail=f"Muitas tentativas falhas. Tente novamente em {remaining} minutos."
            )

    user = db.query(models.User).filter(models.User.email == payload.login).first()

    if not user or not utils.verify_password(payload.password, user.password):

        if user_key not in login_attempts:
            login_attempts[user_key] = {"count": 1, "blocked_until": now}
        else:
            login_attempts[user_key]["count"] += 1
            if login_attempts[user_key]["count"] >= 3:
                login_attempts[user_key]["blocked_until"] = now + timedelta(minutes=10)

        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if user_key in login_attempts:
        del login_attempts[user_key]

    token_str = utils.generate_token(user.email, user.doc_number)
    db.add(models.Token(id_user=user.id, token=token_str))
    user.loggedin = True
    db.commit()

    return {"token": token_str, "user_id": user.id, "message": "Login realizado com sucesso"}

@router.post("/recuperar-senha")
def recover(payload: schemas.PasswordRecovery, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.email,
        models.User.doc_number == payload.document
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.password = utils.hash_password(payload.new_password)
    db.commit()

    token_str = utils.generate_token(user.email, user.doc_number)
    db.add(models.Token(id_user=user.id, token=token_str))
    db.commit()

    return {"token": token_str, "message": "Senha alterada com sucesso"}

@router.post("/logout")
def logout(Authorization: str = Header(None), db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token == Authorization).first()
    if not token:
        raise HTTPException(status_code=400, detail="Token inválido")

    user = db.query(models.User).filter(models.User.id == token.id_user).first()
    user.loggedin = False
    db.commit()

    return {"message": "Logout realizado com sucesso"}

@router.get("/me")
def get_user_data(Authorization: str = Header(None), db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token == Authorization).first()
    if not token:
        raise HTTPException(status_code=400, detail="Token inválido")

    user = db.query(models.User).filter(models.User.id == token.id_user).first()
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "doc_number": user.doc_number,
        "loggedin": user.loggedin
    }
