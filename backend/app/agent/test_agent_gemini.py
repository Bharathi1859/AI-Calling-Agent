from app.agent.state import ConversationState
from app.agent.agent import CallingAgent


state = ConversationState(
    customer_name="Rahul Kumar",
    company_name="ABC Hotels",
    requirement="Commercial RO System"
)

agent = CallingAgent(state)


customer_message = (
    "We need a 500 LPH RO system for our hotel in Bangalore. "
    "Our budget is around 3 lakhs and we want to install it next month."
)


result = agent.process_message(customer_message)


print("\nCustomer Message:")
print(customer_message)

print("\nExtracted Information:")
print(result["extracted_data"])

print("\nUpdated Conversation State:")
print(result["conversation_state"])

print("\nMissing Fields:")
print(result["missing_fields"])

print("\nAgent Response:")
print(result["agent_response"])