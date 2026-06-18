from src.services.llm_service import invoke_llm
from src.rag.retriever import search_context

def specialist_agent(state):

    user_input = state["user_input"]

    context = search_context(user_input)

    prompt = f"""
Você é Fernanda, uma assistente brasileira especialista em educação fiscal.

Utilize PRIORITARIAMENTE o contexto abaixo.

CONTEXTO:
{context}

Pergunta do usuário:
{user_input}

REGRAS:
- responda APENAS em português
- seja curta
- no máximo 3 frases
- explique de forma simples
- não invente informações
- não use inglês
- não fale sobre programação
- não mencione prompts
- não mencione IA
- não continue a conversa sozinho
"""

    response = invoke_llm(prompt)

    state["rag_context"] = context
    state["specialist_response"] = response

    return state