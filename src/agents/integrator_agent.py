def integrator_agent(state):

    specialist_response = state["specialist_response"]

    evaluation = state["evaluation"]

    final_response = f"""
📘 Explicação:

{specialist_response}

🧠 Pergunta para praticar:

{evaluation}
"""

    state["final_response"] = final_response

    return state