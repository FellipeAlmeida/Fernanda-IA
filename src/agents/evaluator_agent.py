from src.services.llm_service import invoke_llm


def evaluator_agent(state):
    """
    O Avaliador só corrige exercícios e fornece feedback.
    (Quem propõe o exercício é o Professor Especialista.)
    """

    intent = state.get("intent")

    if intent != "responder_exercicio":
        return {}

    exercise = state.get("exercise", "")
    expected_answer = state.get("expected_answer", "")
    user_input = state.get("user_input", "")

    # Sem gabarito, a correção ficaria inventada: avisa o aluno.
    if not exercise:
        return {
            "evaluation": (
                "Não encontrei nenhum exercício pendente para corrigir. "
                "Se quiser praticar, é só me pedir um exercício!"
            ),
            "exercise_pending": False,
        }

    prompt = f"""
    Você é uma professora especialista em educação fiscal.

    Avalie a resposta do aluno.

    EXERCÍCIO:
    {exercise}

    GABARITO:
    {expected_answer}

    RESPOSTA DO ALUNO:
    {user_input}

    REGRAS:
        - Compare a resposta do aluno (pode ser uma letra ou o texto da
        alternativa) com o gabarito.
        - Diga logo no início se está correta ou incorreta.
        - Se estiver incorreta, explique de forma simples por que a
        alternativa certa é a do gabarito.
        - Seja breve (no máximo 3 frases) e incentive o aluno.
        - Não crie novas perguntas.
        - Responda em português brasileiro.
    """

    evaluation = invoke_llm(prompt)

    return {
        "evaluation": evaluation.strip(),
        # O exercício foi respondido, então deixa de estar pendente.
        "exercise_pending": False,
    }