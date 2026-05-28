from src.services.llm_service import invoke_llm

def pedagogical_agent(state):

    user_input = state["user_input"]

    prompt = f"""
    Você é um professor de educação fiscal.

    Identifique o tema da pergunta.

    Pergunta:
    {user_input}

    Responda SOMENTE:
    impostos
    ou
    educacao_financeira
    """

    response = invoke_llm(prompt)

    state["topic"] = response.strip()

    return state