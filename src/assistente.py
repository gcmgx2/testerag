import os
import re
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from src.prompts import INTENT_PROMPT, RESPOSTA_PROMPT
from src.rag_system import RAGSystem

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o modelo da LangChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

# Instância do sistema RAG
rag = RAGSystem()

def classificar_intencao(pergunta: str) -> str:
    mensagens = [
        HumanMessage(content=INTENT_PROMPT.format(pergunta=pergunta))
    ]
    resposta = llm.invoke(mensagens)
    return resposta.content.strip().lower()


def gerar_resposta(pergunta: str) -> str:
    intencao = classificar_intencao(pergunta)
    print(f"Intenção classificada: {intencao}")

    if intencao == "produto":
        resultados = rag.buscar_produtos(pergunta)
        contexto = "\n".join([f"- {p['nome']}: {p['descricao']} (R${p.get('preco', 'N/A')})" for p in resultados])

    elif intencao == "pedido":
        pedido_id = extrair_id_pedido(pergunta)
        print(f"pedido_id: {pedido_id}")
        pedido = rag.buscar_pedido_por_id(pedido_id)
        if pedido:
            contexto = f"Status do pedido {pedido['pedido_id']}: {pedido['status']}."
        else:
            contexto = f"Não encontrei informações para o pedido {pedido_id}."

    elif intencao == "politica":
        trechos = rag.buscar_politicas(pergunta)
        contexto = "\n".join(trechos)

    else:
        contexto = "Desculpe, não consegui entender sua pergunta."

    prompt_final = RESPOSTA_PROMPT.format(pergunta=pergunta, contexto=contexto)

    mensagens = [
        HumanMessage(content=prompt_final)
    ]
    resposta = llm.invoke(mensagens)
    return resposta.content.strip()


def extrair_id_pedido(texto: str) -> str:
    match = re.search(r"\b\d{4,}\b", texto)
    return match.group(0) if match else ""
