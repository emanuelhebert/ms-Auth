from fastapi import FastAPI
from .database import Base, engine
from .routes import auth_routes

app = FastAPI(title="API de Autenticação")

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
