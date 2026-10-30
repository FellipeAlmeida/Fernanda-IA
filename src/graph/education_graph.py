from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.utils.state import AgentState

from src.agents.fernanda_agent import pedagogical_agent
from src.agents.specialist_agent import specialist_agent
from src.agents.evaluator_agent import evaluator_agent
from src.agents.integrator_agent import integrator_agent


# --------------------------------- ROTEAMENTO APÓS FERNANDA ---------------------------------


def route_by_intent(state: AgentState) -> str:

    intent = state.get("intent")

    routes = {
        "conversa": "integrator",
        "licao": "specialist",
        "duvida": "specialist",
        "solicitar_exercicio": "specialist",
        "responder_exercicio": "evaluator",
        "feedback": "integrator",
    }

    next_node = routes.get(intent)

    if next_node is None:
        raise ValueError(
            f"Intenção desconhecida ou inválida: {intent}"
        )

    print(f"[ROTEAMENTO] Intenção: {intent} -> Agente: {next_node}")

    return next_node


# --------------------------------- ROTEAMENTO APÓS INTEGRADOR ---------------------------------


def route_after_integrator(state: AgentState) -> str:
    """
    Revisão de Outputs: se o Integrador reprovou o resultado,
    volta ao Professor Especialista. Caso contrário, finaliza.
    """
    if state.get("needs_revision"):
        print("[ROTEAMENTO] Integrador -> Professor Especialista (revisão)")
        return "specialist"

    return "end"


# --------------------------------- CONSTRUÇÃO DO GRAFO ---------------------------------


graph = StateGraph(AgentState)

# Registro dos agentes
graph.add_node("pedagogical", pedagogical_agent)
graph.add_node("specialist", specialist_agent)
graph.add_node("evaluator", evaluator_agent)
graph.add_node("integrator", integrator_agent)

graph.set_entry_point("pedagogical")

# Fernanda decide o próximo agente
graph.add_conditional_edges(
    "pedagogical",
    route_by_intent,
    {
        "specialist": "specialist",
        "evaluator": "evaluator",
        "integrator": "integrator",
    },
)

# Professor Especialista (lições, dúvidas e exercícios) -> Integrador
graph.add_edge("specialist", "integrator")

# Avaliador (correção + feedback) -> Integrador
graph.add_edge("evaluator", "integrator")

# Integrador finaliza ou devolve ao Especialista para revisão
graph.add_conditional_edges(
    "integrator",
    route_after_integrator,
    {
        "specialist": "specialist",
        "end": END,
    },
)

# Checkpointer: mantém o exercício pendente entre as mensagens do aluno
memory = MemorySaver()

app = graph.compile(checkpointer=memory)