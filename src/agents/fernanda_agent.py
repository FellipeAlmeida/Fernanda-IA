import json
import re

from src.services.llm_service import invoke_llm

VALID_TOPICS = {"impostos", "educacao_financeira"}

VALID_INTENTS = {
    "conversa",
    "licao",
    "duvida",
    "solicitar_exercicio",
    "responder_exercicio",
    "feedback",
}

# Reconhece respostas de múltipla escolha como:
# "b", "B)", "(b)", "letra b", "alternativa C", "a resposta é b", "opção a"
ANSWER_PATTERN = re.compile(
    r"^\s*"
    r"(?:(?:a\s+)?(?:resposta|alternativa|letra|op[cç][aã]o)"
    r"\s*(?:é|e|seria|correta)?\s*[:\-]?\s*)?"
    r"\(?([abc])\)?\s*[\.\)!]?\s*$",
    flags=re.IGNORECASE,
)


def is_letter_answer(text: str) -> bool:
    return bool(ANSWER_PATTERN.match(text or ""))


def pedagogical_agent(state):
    user_input = state["user_input"]

    has_pending = bool(state.get("exercise_pending"))
    pending_exercise = state.get("exercise", "") if has_pending else ""

    # Reseta os controles de revisão a cada novo turno.
    base_update = {
        "needs_revision": False,
        "revision_attempts": 0,
    }

    # ---------------- Regra determinística (antes do LLM) ----------------
    # Há exercício pendente e o aluno mandou uma alternativa: é uma resposta.
    if has_pending and is_letter_answer(user_input):
        print("[GUARDA] Alternativa detectada com exercício pendente -> responder_exercicio")
        return {
            "topic": state.get("topic", "impostos"),
            "intent": "responder_exercicio",
            **base_update,
        }

    if has_pending:
        pending_block = f"""
        EXERCÍCIO PENDENTE (já apresentado ao aluno, ainda sem resposta):
        {pending_exercise}
        """
    else:
        pending_block = """
        EXERCÍCIO PENDENTE: nenhum.
        """

    prompt = f"""
        Você é a Fernanda, uma professora especialista em educação fiscal.

        Sua tarefa é APENAS classificar a mensagem do aluno em:

        1. TEMA:
        - impostos
        - educacao_financeira

        2. INTENÇÃO (escolha exatamente uma):

        - conversa:
            Saudações (olá, oi, bom dia), agradecimentos, despedidas ou
            mensagens sem pedido claro de conteúdo.
            Exemplos: "olá", "oi", "tudo bem?", "obrigado", "ok".

        - licao:
            O aluno quer aprender/estudar um conteúdo.
            Exemplo: "Quero aprender sobre impostos".

        - duvida:
            O aluno faz uma pergunta conceitual ou diz que não entendeu.
            Exemplo: "O que são impostos?", "não entendi".

        - solicitar_exercicio:
            O aluno PEDE EXPLICITAMENTE exercícios, atividades, questões
            ou diz que quer praticar/treinar.
            Exemplos: "Me passe exercícios sobre impostos",
            "Quero praticar sobre educação fiscal".

        - responder_exercicio:
            SOMENTE se houver exercício pendente (veja abaixo) e a mensagem
            for uma tentativa de resposta a ele: uma letra (A, B, C), o
            texto de uma alternativa ou uma resposta escrita pelo aluno.
            Se NÃO houver exercício pendente, NUNCA use esta intenção.

        - feedback:
            O aluno comenta ou avalia a experiência de uso do sistema.

        {pending_block}

        REGRAS IMPORTANTES:
        - Uma saudação simples como "olá" é SEMPRE "conversa".
        - NUNCA classifique como solicitar_exercicio se o aluno não pediu
          exercício/prática de forma explícita.
        - Com exercício pendente, uma mensagem curta que responda à pergunta
          (letra ou texto de alternativa) é "responder_exercicio".
        - Com exercício pendente, "não entendi" ou "explica de novo" é "duvida".
        - Não classifique como responder_exercicio só porque a mensagem
          contém a palavra "exercício".
        - Considere o significado da mensagem, não palavras isoladas.
        - Não responda à pergunta do aluno. Apenas classifique.

        Mensagem do aluno:
        {user_input}

        Retorne SOMENTE um JSON válido, sem Markdown ou explicações,
        usando exatamente esta estrutura:

        {{
            "topic": "impostos",
            "intent": "duvida"
        }}
        """

    response = invoke_llm(prompt).strip()

    # Tratamento para o caso de o LLM incluir texto antes ou depois do JSON.
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"A Fernanda não retornou um JSON válido: {response}")

    classification = json.loads(response[start:end + 1])

    topic = classification.get("topic")
    intent = classification.get("intent")

    # Tema inválido não é crítico: usa o padrão.
    if topic not in VALID_TOPICS:
        topic = "impostos"

    if intent not in VALID_INTENTS:
        raise ValueError(
            f"Intenção inválida retornada pela Fernanda: {intent}"
        )

    # ---------------- Guardas determinísticas ----------------

    # Não há exercício pendente: não existe o que corrigir.
    if intent == "responder_exercicio" and not has_pending:
        print("[GUARDA] responder_exercicio sem exercício pendente -> duvida")
        intent = "duvida"

    return {
        "topic": topic,
        "intent": intent,
        **base_update,
    }