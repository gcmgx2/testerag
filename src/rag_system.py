import os
import json
import faiss
import numpy as np
from typing import List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Caminhos dos arquivos de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PRODUTOS_PATH = os.path.join(DATA_DIR, "produtos.json")
PEDIDOS_PATH = os.path.join(DATA_DIR, "pedidos.json")
POLITICAS_PATH = os.path.join(DATA_DIR, "politicas.md")

# Modelo de embedding
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = 1536


def gerar_embedding(texto: str) -> np.ndarray:
    response = client.embeddings.create(
        input=[texto],
        model=EMBEDDING_MODEL
    )
    vetor = response.data[0].embedding
    return np.array(vetor, dtype=np.float32)


def carregar_json(path: str) -> List[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_texto(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class RAGSystem:
    def __init__(self):
        # Carregar dados
        self.produtos = carregar_json(PRODUTOS_PATH)
        self.pedidos = carregar_json(PEDIDOS_PATH)
        self.politicas = carregar_texto(POLITICAS_PATH)

        # Indexar dados vetoriais
        self.index_produtos, self.map_produtos = self._indexar_produtos()
        self.index_politicas, self.map_politicas = self._indexar_politicas()

    def _indexar_produtos(self) -> Tuple[faiss.IndexFlatL2, List[str]]:
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        id_map = []

        for p in self.produtos:
            texto = f"{p['nome']}. {p['descricao']}. Preço: R${p.get('preco', 'N/A')}"
            emb = gerar_embedding(texto)
            index.add(np.array([emb]))
            id_map.append(p["id"])

        return index, id_map

    def _indexar_politicas(self) -> Tuple[faiss.IndexFlatL2, List[str]]:
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        id_map = []

        partes = self.politicas.split("\n\n")
        for i, parte in enumerate(partes):
            emb = gerar_embedding(parte)
            index.add(np.array([emb]))
            id_map.append(parte)

        return index, id_map

    def buscar_produtos(self, consulta: str, top_k: int = 3) -> List[dict]:
        query_emb = gerar_embedding(consulta)
        D, I = self.index_produtos.search(np.array([query_emb]), top_k)
        resultados = []

        for idx in I[0]:
            prod_id = self.map_produtos[idx]
            prod = next(p for p in self.produtos if p["id"] == prod_id)
            resultados.append(prod)

        return resultados

    def buscar_politicas(self, consulta: str, top_k: int = 2) -> List[str]:
        query_emb = gerar_embedding(consulta)
        D, I = self.index_politicas.search(np.array([query_emb]), top_k)
        return [self.map_politicas[idx] for idx in I[0]]

    def buscar_pedido_por_id(self, pedido_id: str) -> dict:
        return next((p for p in self.pedidos if p.get("pedido_id") == pedido_id), None)
