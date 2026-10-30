MAX_REVISIONS = 2

GREETING = (
    "Olá! Eu sou a Fernanda, sua assistente de educação fiscal. 😊\n\n"
    "Posso te explicar uma lição, tirar dúvidas ou propor exercícios "
    "para você praticar. Sobre o que você gostaria de falar?"
)


def _find_problem(state) -> bool:
    """
    Revisão de Outputs: verifica se o que o Especialista entregou
    é utilizável. Retorna True se precisa ser refeito.
    """
    intent = state.get("intent")

    if intent in ("licao", "duvida"):
        return not (state.get("specialist_response") or "").strip()

    if intent == "solicitar_exercicio":
        has_intro = bool((state.get("specialist_response") or "").strip())
        has_exercise = bool((state.get("exercise") or "").strip())
        has_answer = bool((state.get("expected_answer") or "").strip())
        return not (has_intro and has_exercise and has_answer)

    return False


def integrator_agent(state):

    intent = state.get("intent")

    specialist_response = state.get("specialist_response")
    evaluation = state.get("evaluation")
    feedback = state.get("feedback")
    exercise = state.get("exercise")

    # ---------------- Revisão de outputs ----------------
    attempts = state.get("revision_attempts", 0)

    if _find_problem(state):

        if attempts < MAX_REVISIONS:
            print(
                f"[INTEGRADOR] Output inválido. Solicitando revisão "
                f"({attempts + 1}/{MAX_REVISIONS})"
            )
            return {
                "needs_revision": True,
                "revision_attempts": attempts + 1,
            }

        print("[INTEGRADOR] Revisões esgotadas. Usando mensagem de fallback.")
        return {
            "needs_revision": False,
            "exercise_pending": False,
            "final_response": (
                "Desculpe, não consegui preparar essa resposta agora. "
                "Pode tentar reformular o pedido?"
            ),
        }

    # ---------------- Montagem da resposta final ----------------
    if intent == "conversa":

        final_response = GREETING

    elif intent in ["licao", "duvida"]:

        final_response = specialist_response

    elif intent == "solicitar_exercicio":

        final_response = (
            f"{specialist_response}\n\n"
            f"**Exercício:**\n{exercise}"
        )

    elif intent == "responder_exercicio":

        final_response = evaluation or (
            "Não foi possível avaliar sua resposta."
        )

    elif intent == "feedback":

        final_response = (
            "Obrigado pelo seu feedback! "
            "Sua opinião é importante para melhorar nossa experiência."
        )

    else:

        final_response = (
            specialist_response
            or evaluation
            or feedback
            or "Não consegui processar sua solicitação."
        )

    return {
        "needs_revision": False,
        "final_response": final_response,
    }