# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.agent.agent import CallingAgent
# from app.agent.state import ConversationState
# from app.agent.conversation_service import process_customer_message
# from app.conversation_schemas import CustomerMessageRequest, AgentResponse

# from app.database import get_db
# from app.models.call import Call
# from app.models.conversation import ConversationMessage
# from app.conversation_schemas import (
#     ConversationMessageCreate,
#     ConversationMessageResponse
# )


# router = APIRouter(
#     prefix="/conversations",
#     tags=["Conversations"]
# )


# @router.post(
#     "",
#     response_model=ConversationMessageResponse,
#     status_code=201
# )
# def create_message(
#     message_data: ConversationMessageCreate,
#     db: Session = Depends(get_db)
# ):
#     call = (
#         db.query(Call)
#         .filter(Call.id == message_data.call_id)
#         .first()
#     )

#     if not call:
#         raise HTTPException(
#             status_code=404,
#             detail="Call not found"
#         )

#     message = ConversationMessage(
#         call_id=message_data.call_id,
#         speaker=message_data.speaker,
#         message=message_data.message
#     )

#     db.add(message)
#     db.commit()
#     db.refresh(message)

#     return message


# @router.get(
#     "/call/{call_id}",
#     response_model=list[ConversationMessageResponse]
# )
# def get_call_messages(
#     call_id: int,
#     db: Session = Depends(get_db)
# ):
#     call = (
#         db.query(Call)
#         .filter(Call.id == call_id)
#         .first()
#     )

#     if not call:
#         raise HTTPException(
#             status_code=404,
#             detail="Call not found"
#         )

#     messages = (
#         db.query(ConversationMessage)
#         .filter(ConversationMessage.call_id == call_id)
#         .order_by(ConversationMessage.timestamp.asc())
#         .all()
#     )

#     return messages

# @router.post(
#     "/call/{call_id}/message",
#     response_model=AgentResponse
# )
# def process_message(
#     call_id: int,
#     message_data: CustomerMessageRequest,
#     db: Session = Depends(get_db)
# ):
#     call = (
#         db.query(Call)
#         .filter(Call.id == call_id)
#         .first()
#     )

#     if not call:
#         raise HTTPException(
#             status_code=404,
#             detail="Call not found"
#         )

#     customer = call.customer

#     state = ConversationState(
#         customer_name=customer.name,
#         company_name=customer.company_name,
#         requirement=customer.product
#     )

#     agent = CallingAgent(state)

#     result = process_customer_message(
#         db=db,
#         call_id=call_id,
#         agent=agent,
#         customer_message=message_data.message
#     )

#     return {
#         "call_id": call_id,
#         "customer_message": message_data.message,
#         "agent_response": result["agent_response"],
#         "conversation_state": result["conversation_state"],
#         "missing_fields": result["missing_fields"]
#     }


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.call import Call
from app.models.conversation import ConversationMessage

from app.conversation_schemas import (
    ConversationMessageCreate,
    ConversationMessageResponse,
    CustomerMessageRequest,
    AgentResponse
)

from app.agent.agent import CallingAgent
from app.agent.state_service import (
    load_conversation_state,
    save_conversation_state
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post(
    "",
    response_model=ConversationMessageResponse,
    status_code=201
)
def create_message(
    message_data: ConversationMessageCreate,
    db: Session = Depends(get_db)
):
    call = (
        db.query(Call)
        .filter(Call.id == message_data.call_id)
        .first()
    )

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    message = ConversationMessage(
        call_id=message_data.call_id,
        speaker=message_data.speaker,
        message=message_data.message
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@router.get(
    "/call/{call_id}",
    response_model=list[ConversationMessageResponse]
)
def get_call_messages(
    call_id: int,
    db: Session = Depends(get_db)
):
    call = (
        db.query(Call)
        .filter(Call.id == call_id)
        .first()
    )

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    messages = (
        db.query(ConversationMessage)
        .filter(ConversationMessage.call_id == call_id)
        .order_by(ConversationMessage.timestamp.asc())
        .all()
    )

    return messages


@router.post(
    "/call/{call_id}/message",
    response_model=AgentResponse
)
def process_message(
    call_id: int,
    message_data: CustomerMessageRequest,
    db: Session = Depends(get_db)
):
    # Find the call
    call = (
        db.query(Call)
        .filter(Call.id == call_id)
        .first()
    )

    if not call:
        raise HTTPException(
            status_code=404,
            detail="Call not found"
        )

    # Get customer information
    customer = call.customer

    # Load previous conversation state from PostgreSQL
    state = load_conversation_state(
        db=db,
        call_id=call_id,
        customer_name=customer.name,
        company_name=customer.company_name,
        default_requirement=customer.product
    )

    # Create AI agent using the persisted state
    agent = CallingAgent(state)

    # Save customer message
    customer_message = ConversationMessage(
        call_id=call_id,
        speaker="customer",
        message=message_data.message
    )

    db.add(customer_message)
    db.commit()

    # Process the new message
    result = agent.process_message(
        message_data.message
    )

    # Save updated state to PostgreSQL
    save_conversation_state(
        db=db,
        call_id=call_id,
        state=agent.state
    )

    # Save AI response
    ai_message = ConversationMessage(
        call_id=call_id,
        speaker="ai",
        message=result["agent_response"]
    )

    db.add(ai_message)
    db.commit()

    return {
        "call_id": call_id,
        "customer_message": message_data.message,
        "agent_response": result["agent_response"],
        "conversation_state": result["conversation_state"],
        "missing_fields": result["missing_fields"]
    }