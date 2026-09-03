from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bancodados import criar_banco
from routers import metas, transacoes, criar_login

app = FastAPI(title="Nexus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

criar_banco()

app.include_router(metas.router)
app.include_router(transacoes.router)
app.include_router(criar_login.router)

@app.get("/")
def raiz():
    return {"status": "API rodando 100%!"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}
