import re

from src.services.llm_service import invoke_llm
from src.rag.retriever import search_context


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def parse_exercise(text: str):
    """
    Espera um texto no formato:

        PERGUNTA: ...
        A) ...
        B) ...
        C) ...
        GABARITO: B - explicação curta

    Retorna (exercicio, gabarito). Se o formato não for respeitado,
    retorna ("", "") e o Integrador pede uma revisão.
    """
    match = re.search(r"GABARITO\s*:", text, flags=re.IGNORECASE)

    if not match:
        return "", ""

    exercise = text[:match.start()].strip()
    expected = text[match.end():].strip()

    exercise = re.sub(r"^\s*PERGUNTA\s*:\s*", "", exercise, flags=re.IGNORECASE)

    # Valida: precisa ter pelo menos as alternativas A, B e C.
    has_options = all(
        re.search(rf"(^|\n)\s*{letter}\)", exercise)
        for letter in ("A", "B", "C")
    )

    if not exercise or not expected or not has_options:
        return "", ""

    return exercise, expected


COMMON_RULES = """
REGRAS:
- Responda somente em português brasileiro.
- Use linguagem simples, como se explicasse para um estudante do ensino médio.
- Utilize prioritariamente o contexto fornecido.
- Não invente informações.
- Não comece com saudação (nada de "Olá" ou "Estou aqui para ajudar").
- Não fale sobre programação.
- Não mencione prompts ou inteligência artificial.
- Não continue a conversa sozinho.
"""


# ---------------------------------------------------------------------------
# Exercício (duas etapas)
# ---------------------------------------------------------------------------

def build_exercise(user_input: str, topic: str, context: str):
    # Etapa 1: introdução simples, só com o conceito mais básico
    intro_prompt = f"""
    Você é Fernanda, uma professora brasileira de educação fiscal.

    TEMA: {topic}

    CONTEXTO DA BASE DE CONHECIMENTO:
    {context}

    O aluno pediu para praticar: "{user_input}"

    TAREFA:
    Escreva uma introdução curta (3 a 4 frases) explicando apenas a
    IDEIA MAIS BÁSICA do tema, para quem está começando.

    - Escolha UM conceito simples (ex.: o que é imposto e para que serve).
    - IGNORE detalhes técnicos do contexto (siglas como ICMS, contribuinte
      de fato/de direito, emendas, leis, artigos).
    - Dê um exemplo do dia a dia (escola, saúde, transporte, compras).
    - Não faça perguntas.
    {COMMON_RULES}
    """

    intro = invoke_llm(intro_prompt).strip()

    # Etapa 2: exercício fácil, baseado SOMENTE na introdução
    exercise_prompt = f"""
    Você é uma professora brasileira de educação fiscal.

    Crie UMA questão de múltipla escolha FÁCIL, para iniciantes, baseada
    somente no texto abaixo.

    TEXTO:
    {intro}

    REGRAS:
    - A resposta correta deve estar escrita de forma clara no texto.
    - Pergunte sobre uma ideia simples (o que é, para que serve, exemplo).
    - Não use termos técnicos que não estejam no texto.
    - Três alternativas (A, B e C), apenas uma correta.
    - As alternativas erradas devem ser claramente erradas, sem pegadinha.
    - Não dependa de dados pessoais, percentuais ou valores.
    - Responda em português brasileiro.

    Responda EXATAMENTE neste formato, sem nada antes ou depois:

    PERGUNTA: <pergunta>
    A) <alternativa>
    B) <alternativa>
    C) <alternativa>
    GABARITO: <letra> - <explicação em uma frase>
    """

    raw = invoke_llm(exercise_prompt)
    exercise, expected = parse_exercise(raw)

    return intro, exercise, expected


# ---------------------------------------------------------------------------
# Agente
# ---------------------------------------------------------------------------

def specialist_agent(state):

    user_input = state["user_input"]
    intent = state.get("intent", "duvida")
    topic = state.get("topic", "")

    # Busca informações relevantes na base de conhecimento
    context = search_context(user_input)

    # ---------------- Exercício ----------------
    if intent == "solicitar_exercicio":

        intro, exercise, expected = build_exercise(user_input, topic, context)

        return {
            "rag_context": context,
            "specialist_response": intro,
            "exercise": exercise,
            "expected_answer": expected,
            # Só fica pendente se o exercício foi gerado corretamente.
            # Caso contrário, o Integrador aciona a revisão.
            "exercise_pending": bool(exercise and expected),
        }

    # ---------------- Lição e dúvida ----------------
    if intent == "licao":

        task = """
        O aluno deseja estudar um conteúdo.

        Apresente uma explicação didática e curta (no máximo 6 frases).
        Comece pelo conceito mais básico e dê um exemplo do dia a dia.
        """

    elif intent == "duvida":

        pending_exercise = (
            state.get("exercise", "") if state.get("exercise_pending") else ""
        )

        if pending_exercise:
            # Ex.: o aluno disse "não entendi" depois de receber um exercício.
            task = f"""
            O aluno recebeu o exercício abaixo e demonstrou dúvida.

            EXERCÍCIO:
            {pending_exercise}

            Explique de forma mais simples o conceito necessário para
            responder, com um exemplo do dia a dia.
            NÃO revele qual alternativa é a correta.
            Ao final, convide o aluno a tentar responder.
            """
        else:
            task = """
            O aluno possui uma dúvida.

            Responda diretamente à pergunta, de forma simples e objetiva
            (no máximo 5 frases), com um exemplo do dia a dia.
            """

    else:
        task = """
        Analise a solicitação e forneça uma resposta curta
        relacionada à educação fiscal.
        """

    prompt = f"""
    Você é Fernanda, uma assistente brasileira especialista
    em educação fiscal.

    TEMA:
    {topic}

    CONTEXTO DA BASE DE CONHECIMENTO:
    {context}

    MENSAGEM DO ALUNO:
    {user_input}

    TAREFA:
    {task}
    {COMMON_RULES}
    """

    response = invoke_llm(prompt)

    return {
        "rag_context": context,
        "specialist_response": response.strip(),
    }