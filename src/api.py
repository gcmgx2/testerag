import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from src.assistente import gerar_resposta

# Inicializa a aplicação FastAPI com título personalizado
app = FastAPI(title="Assistente Virtual para E-commerce")

# Middleware CORS para permitir acesso do frontend (ajuste os domínios conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, use ["http://seusite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para os arquivos de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# Modelo da requisição POST /chat
class Consulta(BaseModel):
    pergunta: str


# Endpoint principal: envia pergunta ao assistente virtual
@app.post("/chat")
async def chat(consulta: Consulta):
    try:
        resposta = gerar_resposta(consulta.pergunta)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para visualizar produtos.json
@app.get("/dados/produtos")
def get_produtos():
    try:
        path = os.path.join(DATA_DIR, "produtos.json")
        with open(path, encoding="utf-8") as f:
            produtos = json.load(f)
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para visualizar pedidos.json
@app.get("/dados/pedidos")
def get_pedidos():
    try:
        path = os.path.join(DATA_DIR, "pedidos.json")
        with open(path, encoding="utf-8") as f:
            pedidos = json.load(f)
        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint para visualizar politicas.md (como texto plano)
@app.get("/dados/politicas")
def get_politicas():
    try:
        path = os.path.join(DATA_DIR, "politicas.md")
        with open(path, encoding="utf-8") as f:
            politicas = f.read()
        return PlainTextResponse(content=politicas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
