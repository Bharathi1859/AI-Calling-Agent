from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationMessageCreate(BaseModel):
    call_id: int
    speaker: str
    message: str


class ConversationMessageResponse(BaseModel):
    id: int
    call_id: int
    speaker: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class CustomerMessageRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    call_id: int
    customer_message: str
    agent_response: str
    conversation_state: dict
    missing_fields: list[str]