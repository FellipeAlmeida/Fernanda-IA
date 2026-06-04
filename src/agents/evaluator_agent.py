from src.services.llm_service import invoke_llm

def evaluator_agent(state):

    response = state["specialist_response"]

    prompt = f"""
Você é uma professora brasileira.

Crie UMA pergunta curta em português baseada na explicação abaixo.

REGRAS:
- apenas 1 pergunta
- sem resposta
- sem explicações extras
- sem inglês
- seja objetiva
- faça perguntas apenas sobre as informações fornecidas pelo especialista

Explicação:
{response}
"""

    evaluation = invoke_llm(prompt)

    state["evaluation"] = evaluation

    return state