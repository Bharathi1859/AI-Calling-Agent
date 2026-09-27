from app.agent.state import ConversationState
from app.agent.agent import CallingAgent


state = ConversationState(
    customer_name="Rahul Kumar",
    company_name="ABC Hotels",
    requirement="Commercial RO System"
)

agent = CallingAgent(state)

print("Conversation State:")
print(state.to_dict())

print("\nMissing Fields:")
print(agent.get_missing_fields())

print("\nAgent Response:")
print(agent.generate_response())