# from app.agent.state import ConversationState


# class CallingAgent:

#     def __init__(self, state: ConversationState):
#         self.state = state

#     def get_missing_fields(self):
#         required_fields = [
#             "requirement",
#             "capacity",
#             "location",
#             "application",
#             "budget",
#             "timeline"
#         ]

#         state_data = self.state.to_dict()

#         missing = []

#         for field in required_fields:
#             if not state_data.get(field):
#                 missing.append(field)

#         return missing

#     def generate_response(self):
#         missing = self.get_missing_fields()

#         if "requirement" in missing:
#             return "Could you please tell me what product or service you are looking for?"

#         if "capacity" in missing:
#             return "Could you tell me the required capacity?"

#         if "location" in missing:
#             return "Could you tell me the location where the product will be installed?"

#         if "application" in missing:
#             return "Could you tell me what the product will be used for?"

#         if "budget" in missing:
#             return "Do you have an approximate budget in mind?"

#         if "timeline" in missing:
#             return "When are you planning to purchase or install the product?"

#         return "Thank you. I have collected all the required information. Our team will review your requirements and get back to you."

import json
import os

from dotenv import load_dotenv
from google import genai

from app.agent.state import ConversationState


load_dotenv()


class CallingAgent:

    def __init__(self, state: ConversationState):
        self.state = state

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")

        self.client = genai.Client(api_key=api_key)

    def get_missing_fields(self):
        required_fields = [
            "requirement",
            "capacity",
            "location",
            "application",
            "budget",
            "timeline"
        ]

        state_data = self.state.to_dict()

        missing = []

        for field in required_fields:
            if not state_data.get(field):
                missing.append(field)

        return missing

    def extract_information(self, customer_message: str):
        current_state = self.state.to_dict()

        prompt = f"""
You are an AI calling agent for a business sales enquiry.

Your job is to extract useful customer information from the customer's message.

Current conversation state:
{json.dumps(current_state, indent=2)}

Customer message:
"{customer_message}"

Extract only information that is explicitly stated or clearly provided by the customer.

Return ONLY valid JSON with these fields:

{{
    "requirement": null,
    "capacity": null,
    "location": null,
    "application": null,
    "budget": null,
    "timeline": null
}}

Rules:
- Do not invent information.
- If a field is not mentioned, return null.
- Preserve useful units such as LPH, liters, kg, etc.
- Keep the values concise.
"""

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        response_text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        try:
            extracted_data = json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError(
                f"Gemini returned invalid JSON: {response_text}"
            )

        return extracted_data

    def update_state(self, extracted_data):
        fields = [
            "requirement",
            "capacity",
            "location",
            "application",
            "budget",
            "timeline"
        ]

        for field in fields:
            value = extracted_data.get(field)

            if value:
                setattr(self.state, field, value)

    def generate_response(self):
        missing = self.get_missing_fields()

        if "requirement" in missing:
            return "Could you please tell me what product or service you are looking for?"

        if "capacity" in missing:
            return "Could you tell me the required capacity?"

        if "location" in missing:
            return "Could you tell me the location where the product will be installed?"

        if "application" in missing:
            return "Could you tell me what the product will be used for?"

        if "budget" in missing:
            return "Do you have an approximate budget in mind?"

        if "timeline" in missing:
            return "When are you planning to purchase or install the product?"

        return (
            "Thank you. I have collected all the required information. "
            "Our team will review your requirements and get back to you."
        )

    def process_message(self, customer_message: str):
        extracted_data = self.extract_information(customer_message)

        self.update_state(extracted_data)

        response = self.generate_response()

        return {
            "extracted_data": extracted_data,
            "conversation_state": self.state.to_dict(),
            "missing_fields": self.get_missing_fields(),
            "agent_response": response
        }