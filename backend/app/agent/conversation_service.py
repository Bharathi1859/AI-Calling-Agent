from sqlalchemy.orm import Session

from app.agent.agent import CallingAgent
from app.agent.state import ConversationState
from app.models.conversation import ConversationMessage


def save_message(
    db: Session,
    call_id: int,
    speaker: str,
    message: str
):
    conversation_message = ConversationMessage(
        call_id=call_id,
        speaker=speaker,
        message=message
    )

    db.add(conversation_message)
    db.commit()
    db.refresh(conversation_message)

    return conversation_message


def process_customer_message(
    db: Session,
    call_id: int,
    agent: CallingAgent,
    customer_message: str
):
    # Save customer message
    save_message(
        db=db,
        call_id=call_id,
        speaker="customer",
        message=customer_message
    )

    # Process message using AI agent
    result = agent.process_message(customer_message)

    # Save AI response
    save_message(
        db=db,
        call_id=call_id,
        speaker="ai",
        message=result["agent_response"]
    )

    return result