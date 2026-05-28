from src.services.llm_service import invoke_llm

def specialist_agent(state):

    user_input = state["user_input"]

    prompt = f"""
Você é Fernanda, uma assistente brasileira especialista em educação fiscal.

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

Pergunta do usuário:
{user_input}
"""

    response = invoke_llm(prompt)

    state["specialist_response"] = response

    return state