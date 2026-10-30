from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):  # total=False: o estado é preenchido gradualmente
    user_input: str

    topic: str
    intent: str

    # Contexto e resultados dos agentes
    rag_context: str
    specialist_response: str
    evaluation: str
    feedback: str
    final_response: str

    # Exercício em andamento (persiste entre turnos via checkpointer)
    exercise: str
    expected_answer: str
    exercise_pending: bool

    # Revisão de outputs (Integrador -> Especialista)
    needs_revision: bool
    revision_attempts: int

    conversation_id: Optional[int]
    user_id: Optional[int]