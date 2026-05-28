from langgraph.graph import StateGraph, END

from src.agents.integrator_agent import integrator_agent
from src.utils.state import AgentState

from src.agents.fernanda_agent import pedagogical_agent
from src.agents.specialist_agent import specialist_agent
from src.agents.evaluator_agent import evaluator_agent

graph = StateGraph(AgentState)

graph.add_node("pedagogical", pedagogical_agent)
graph.add_node("specialist_agent", specialist_agent)
graph.add_node("evaluator", evaluator_agent)
graph.add_node("integrator", integrator_agent)

graph.set_entry_point("pedagogical")

graph.add_edge("pedagogical", "specialist_agent")
graph.add_edge("specialist_agent", "evaluator")
graph.add_edge("evaluator", "integrator")
graph.add_edge("integrator", END)

app = graph.compile()