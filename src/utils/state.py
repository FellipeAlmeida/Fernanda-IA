from typing import TypedDict, Optional

class AgentState(TypedDict):

    user_input: str

    topic: str

    rag_context: str

    specialist_response: str

    evaluation: str

    final_response: str

    conversation_id: Optional[int]

    user_id: Optional[int]