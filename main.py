from fastapi import FastAPI
from .database import Base, engine
from .routes import auth_routes
from fastapi import Request
from security.throttling import rate_limit

app = FastAPI(title="API de Autenticação")

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    rate_limit(client_ip)
    response = await call_next(request)
    return response
