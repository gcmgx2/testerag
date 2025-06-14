# src/prompts.py

# Prompt para classificação de intenção
INTENT_PROMPT = """
Você é um assistente virtual de uma loja online. Sua tarefa é classificar a intenção da seguinte pergunta feita por um usuário em exatamente uma das categorias abaixo:

- produto: o usuário quer informações, recomendações ou dúvidas sobre produtos da loja (ex: "Qual notebook tem processador i5?", "Me indique um celular barato", "Vocês têm fones sem fio?").
- pedido: o usuário está perguntando sobre status, entrega, ou detalhes de um pedido já realizado (ex: "Onde está meu pedido?", "Quando chega minha compra?", "Posso cancelar meu pedido?").
- politica: o usuário quer informações sobre as políticas da loja, como troca, devolução, pagamento, garantia, atendimento, ou dúvidas institucionais (ex: "Qual a política de devolução?", "Como funciona a garantia?", "Qual o telefone do suporte?").

Pergunta: "{pergunta}"

Responda **somente** com a palavra correta: produto, pedido ou politica.

Se a pergunta for ambígua, escolha a categoria que parecer mais relevante para o atendimento do usuário.

"""

# Prompt para resposta final
RESPOSTA_PROMPT = """
Você é um assistente para e-commerce.

Com base na pergunta do usuário e nas informações abaixo, gere uma resposta clara, educada e útil.

Pergunta: {pergunta}

Informações relevantes:
{contexto}

Resposta:
"""
