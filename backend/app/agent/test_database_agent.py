from app.database import SessionLocal
from app.agent.state import ConversationState
from app.agent.agent import CallingAgent
from app.agent.conversation_service import process_customer_message


db = SessionLocal()


try:
    state = ConversationState(
        customer_name="Rahul Kumar",
        company_name="ABC Hotels"
    )

    agent = CallingAgent(state)

    customer_message = "We need a commercial RO system."

    result = process_customer_message(
        db=db,
        call_id=1,
        agent=agent,
        customer_message=customer_message
    )

    print("\nCustomer:")
    print(customer_message)

    print("\nAgent:")
    print(result["agent_response"])

    print("\nConversation State:")
    print(result["conversation_state"])

    print("\nMissing Fields:")
    print(result["missing_fields"])

finally:
    db.close()