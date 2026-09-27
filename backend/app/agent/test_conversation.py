from app.agent.state import ConversationState
from app.agent.agent import CallingAgent


state = ConversationState(
    customer_name="Rahul Kumar",
    company_name="ABC Hotels"
)

agent = CallingAgent(state)


conversation = [
    "We need a commercial RO system.",
    "The capacity should be around 500 LPH.",
    "It will be installed in Bangalore.",
    "It is for our hotel.",
    "Our budget is around 3 lakhs.",
    "We want to install it next month."
]


print("\n========== AI CALLING AGENT ==========\n")


for customer_message in conversation:

    print("Customer:")
    print(customer_message)

    result = agent.process_message(customer_message)

    print("\nExtracted Information:")
    print(result["extracted_data"])

    print("\nCurrent State:")
    print(result["conversation_state"])

    print("\nMissing Fields:")
    print(result["missing_fields"])

    print("\nAgent:")
    print(result["agent_response"])

    print("\n--------------------------------------\n")


print("========== FINAL CUSTOMER REQUIREMENT ==========\n")

print(agent.state.to_dict())